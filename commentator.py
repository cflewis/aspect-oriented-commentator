#!/usr/bin/env python
# encoding: utf-8
"""
commentator.py

Created by Chris Lewis on 2008-11-10.
Copyright (c) 2008 Chris Lewis. All rights reserved.
"""

import subprocess
import sys
import os
import unittest
import time
from character import *
from springpython.aop import *
from database import *
from lines import Lines
from talker import Talker
import atexit
import random

class CommentatorTalker(object):
    def __init__(self, database):
        self.lines = Lines()
        self.database = database
        self.talker = Talker()
        self.talker.start()
        
    def tag(self, tagger, tagged):
        tag_lines = []
        weighted_tag_lines = []
        tagger_speed = tagger.getActualSpeed()
        tagged_speed = tagged.getActualSpeed()
        tag_line = None
        
        if tagger_speed - tagged_speed > 60:
            tag_lines.append(self.lines.get_fast_tagger_slow_tagged_line())
        elif tagger_speed > 60:
            tag_lines.append(self.lines.get_fast_tagger_line())
        elif tagged_speed < 60:
            tag_lines.append(self.lines.get_slow_tagged_line())
        
        tag_lines.append(self.lines.get_standard_tag_line())
                      
        self.say(random.choice(tag_lines) % {'tagger': tagger.getName(), 'tagged': tagged.getName()})
        print str(tagger_speed) + ", " + str(tagged_speed)
        
        self.check_for_tag_color(tagger, tagged)

    
    def check_for_tag_color(self, tagger, tagged):
        tag_line_strings = []
        
        # cflewis | 2008-11-22 | Say something about the number of tags
        tag_line_strings.append(self.lines.get_number_of_tags_line() \
            % {'tagger': tagger.getName(), 'tagged': tagged.getName(), 'tags': \
            self.database.get_tag_number(tagger.getName(), tagged.getName())})
        
        # cflewis | 2008-11-22 | Say something about the speed of the tagger
        speed_comment = self.get_speed_comment(tagger)
        if speed_comment is not None: tag_line_strings.append(speed_comment)
        speed_comment = self.get_speed_comment(tagged)
        if speed_comment is not None: tag_line_strings.append(speed_comment)
             
        self.say(random.choice(tag_line_strings))
        # cflewis | 2008-11-26 | Shuffle the color commentary and
        # push it to the commentator talking buffer, where it can
        # say these things if it has time to
        #random.shuffle(tag_line_strings)
        
        #while len(tag_line_strings) > 0:
        #    self.say(tag_line_strings.pop())
        
    def get_speed_comment(self, character):
        average_speed = self.database.get_average_speed(character.getName())
        print "Average speed is %s, and actual speed is %s" % (average_speed, character.getActualSpeed())
        
        if character.getActualSpeed() > (average_speed + 10):
            return self.lines.get_faster_than_average_line() % \
                {'character': character.getName(), 'speed': average_speed}
        
        
        if character.getActualSpeed() < (average_speed - 10):
            return self.lines.get_slower_than_average_line() % \
                {'character': character.getName(), 'speed': average_speed}
        
        # cflewis | 2008-11-26 | Nothing interesting to say about this
        return None
        
        
    def say(self, comment):
        print comment
        #os.system('say "' + comment +' " &')
        self.talker.addComment(comment)
        
    def clean_up(self):
        self.talker.end()

class CommentatorGameStateObserver(MethodInterceptor):
    def __init__(self, output_strategy = None, storage_strategy = None):
        self.storage_strategy = storage_strategy
        self.output_strategy = output_strategy
        self.who_tagged = None
        self.was_tagged = None
        self.time_of_last_tag = time.time()
        self.last_tag = None
        self.time_to_tag = 0
        
    def invoke(self, invocation):
        self.last_tag = self.process_tag(invocation)
        
        if self.last_tag:
            time_of_tag = time.time()
            self.time_to_tag = time_of_tag - self.time_of_last_tag
            self.time_of_last_tag = time_of_tag
            self.output_strategy.tag(self.last_tag["tagger"], self.last_tag["tagged"])
            self.storage_strategy.store_game_state(self)

        return invocation.proceed()
        
    def process_tag(self, invocation):
        action = invocation.method_name
        arguments = invocation.args
        
        if action == "setTagged":            
            character_dictionary = {"tagger": arguments[1], "tagged": arguments[0]}
            return character_dictionary
        
        return None
        
    def clean_up(self):
        pass
            

# cflewis | 2008-11-11 | This commentator watches invidiual
# characters
class CommentatorCharacterObserver(MethodInterceptor):
    def __init__(self, output_strategy = None, storage_strategy = None):
        self.storage_strategy = storage_strategy
        self.average_speed = 0
        self.ticks = 0
        self.invocation = None
        
    def invoke(self, invocation):
        if self.invocation is None:
            self.set_instance_variables(invocation)
            
        self.invocation = invocation.instance
        self.calculate_average_speed(invocation.instance.getActualSpeed())
        return invocation.proceed()
        
    def calculate_average_speed(self, current_speed):
        self.average_speed = (current_speed + (self.average_speed * self.ticks)) / (self.ticks + 1)
        self.ticks = self.ticks + 1
        
    def set_instance_variables(self, invocation):
        self.invocation = invocation
        # cflewis | 2008-11-17 | Get data out of DB
        
    def clean_up(self):
        # cflewis | 2008-11-17 | Save data to DB
        self.storage_strategy.store_character(self)


class Commentator:
	def __init__(self):
            self.database = Database()
            self.talker = CommentatorTalker(self.database)
            self.game_state_advisor = CommentatorGameStateObserver(output_strategy = self.talker, storage_strategy = self.database)
            self.observer_list = [self.game_state_advisor]
            atexit.register(self.clean_up)
		
	def get_observed_character(self, character):
            character_advisor = CommentatorCharacterObserver(output_strategy = self.talker, storage_strategy = self.database)
            self.observer_list.append(character_advisor)
            # cflewis | 2008-11-17 | calcAction appears to be the method
            # that provides the actual action *per character*
            pointcutAdvisor = RegexpMethodPointcutAdvisor(advice = [character_advisor], patterns = [".*calcAction.*"])
            return ProxyFactoryObject(target = character, interceptors = pointcutAdvisor)
            
        def get_observed_game_state(self, game_state):
            pointcutAdvisor = RegexpMethodPointcutAdvisor(advice = [self.game_state_advisor], patterns = [".*setTagged.*"])
            return ProxyFactoryObject(target = game_state, interceptors = pointcutAdvisor)
    
        '''A function called when the program needs to clean up. This will cause
        all observers to have their clean up functions called, saving data
        out to the database'''        
        def clean_up(self):
            for observer in self.observer_list:
                observer.clean_up()
            
            self.database.clean_up()
            self.talker.clean_up()               

class CommentatorTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()

