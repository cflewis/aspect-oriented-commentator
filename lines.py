#!/usr/bin/env python
# encoding: utf-8
"""
lines.py

Created by Chris Lewis on 2008-11-22.
Copyright (c) 2008 Chris Lewis. All rights reserved.
"""

import sys
import os
import unittest
import random

class Lines:
    def __init__(self):
        self.standard_tag_lines = [
            "%(tagger)s tagged %(tagged)s.", 
            "%(tagger)s gets the tag on %(tagged)s.",
            "Good work by %(tagger)s, that's a tag on %(tagged)s.",
            "Tag! %(tagged)s loses out to %(tagged)s",
            "Tag! %(tagger)s nails %(tagged)s",
            "And that's a tag on %(tagged)s.",
            "%(tagger)s gets out of there after tagging %(tagged)s",
            "%(tagger)s ups their score by one, putting the hurt on %(tagged)s",
            "The tagging continues, %(tagger)s on %(tagged)s",
            "Another tag. Sometimes I feel like this game of tag is endless",
            "%(tagged)s wasn't able to avoid %(tagger)s",
            "Try as they might %(tagger)s concedes to %(tagged)s",
            "%(tagger)s executes a nifty move, tagging %(tagged)s",
            "%(tagged)s just couldn't get a way from %(tagger)s"
        ]
        
        self.fast_tagger_slow_tagged_lines = [
            "%(tagger)s just slammed %(tagged)s. Ouch!",
            "%(tagger)s levels %(tagged)s, they're going to be remembering that in the morning.",
            "%(tagger)s cleans %(tagged)s 's clock.",
            "%(tagger)s executes a vicious tag on %(tagged)s.",
            "Wham! %(tagged)s gets nailed by %(tagger)s.",
            "%(tagger)s shows no mercy to %(tagged)s, that was a hard hit.",
            "I felt that one from here, %(tagger)s just barrelling into %(tagged)s",
            "%(tagged)s deserved the tag from %(tagger)s for moving so slowly",
            "There's no time to take a breath in this game, %(tagger)s getting a tag on the slower %(tagged)s",
            "%(tagger)s seems to have boundless energy, something the slower %(tagged)s didn't, and grabs a tag.",
            "%(tagged)s got obliterated by %(tagger)s, getting up from that one will be hard",
            "%(tagger)s just puts everything they have into that tag, and %(tagged)s was not expecting it."
        ]
        
        self.fast_tagger_lines = [
            "%(tagger)s builds up a head of steam and gets %(tagged)s.",
            "%(tagger)s just gets the tag with %(tagged)s on the run.",
            "A close race, but %(tagger)s just gets the edge on %(tagged)s",
            "Flat out speed from both competitors, but %(tagger)s stretches just enough to tag %(tagged)s",
            "%(tagger)s finds an extra reserve from somewhere, catching the quick %(tagged)s",
            "%(tagger)s sprints to get %(tagged)s, that's a tag.",
            "%(tagged)s put in a great effort, but %(tagger)s proved they woudln't be denied the tag",
            "Even at top speed, %(tagged)s couldn't avoid %(tagger)s.",
            "An exciting race ends with %(tagger)s getting the tag on %(tagged)s",
            "What a pace! It's unsurprising %(tagged)s couldn't shake %(tagger)s",
            "I got tired just watching that race."
        ]
        
        self.slow_tagged_lines = [
            "%(tagger)s catches %(tagged)s napping, that's a tag.",
            "%(tagger)s shows %(tagged)s can run, but just can't hide in a boundless, endless world of tag.",
            "%(tagger)s gets the unsure %(tagged)s, you gotta be decisive in this game.",
            "%(tagged)s needed to move faster with %(tagger)s on their tail.",
            "%(tagged)s isn't given any breathing space by %(tagger)s.",
            "That's a tag on the slow %(tagged)s",
            "%(tagged)s can't have seen %(tagger)s zeroing in on them, or they would have moved faster.",
            "Speed is of the essence in tag, and %(tagged)s just didn't have it.",
            "I'd be tired in an infinite game of tag, but %(tagged)s has to show the dedication that %(tagger)s exhibited.",
            "%(tagged)s slows down, and %(tagger)s takes advantage and grabs a tag.",
            "%(tagged)s was a sitting duck, leaving the door open for %(tagger)s to get the tag.",
            "%(tagged)s proved to be a little too slow, and %(tagger)s tags them."
        ]
        
        self.number_of_tags_lines = [
            "%(tagger)s brings their lifetime tag total on %(tagged)s to %(tags)d.",
            "%(tagged)s hit by %(tagger)s means that's %(tags)d across all our tag games.",
            "%(tagger)s's rivalry with %(tagged)s heats up with lifetime tag number %(tags)d.",
            "For those of you counting at home, that's number %(tags)s between these two.",
            "Another tag for %(tagger)s, that's %(tags)d against %(tagged)s.",
            "%(tagger)s ups their total to %(tags)d against %(tagged)s.",
            "%(tagged)s concedes another tag to %(tagger)s, that's tag number %(tags)d.",
            "%(tagger)s puts another one on the scoreboard against %(tagged)s, for a score of %(tags)d.",
        ]
        
        self.average_speed_lines = [
            "%(character)s usually moves at %(speed)d."
        ]
        
        self.faster_than_average_lines = [
            "%(character)s was moving faster than usual there.",
            "%(character)s seems to have found a higher gear!",
            "That's a rare burst of speed from %(character)s.",
            "We usually see %(character)s move at %(speed)d, so they're definitely moving faster than usual.",
            "%(character)s turns up the dials during that tag.",
            "I'm not used to seeing %(character)s move so quickly.",
            "A surprising turn of speed for %(character)s.",
            "%(character)s drew up some reserves to find the extra speed during that tag.",
            "%(character)s was moving faster than their usual pace of %(speed)d.",
            "It can't have been easy for %(character)s to summon up that extra speed.",
            "We usually see a speed of about %(speed)d out of %(character)s.",
            "That's some fast moving by the standard of %(character)s."
        ]
        
        self.slower_than_average_lines = [
            "The wind seems to have gone out of the sails of %(character)s.",
            "I wonder if %(character)s is tired? They're certainly moving slower than usual.",
            "%(character)s slows down to catch their breath.",
            "We usually see %(character)s moving at %(speed)d, so they seem to have slowed down.",
            "That's some slow moving for the usually quicker %(character)s.",
            "I don't know if it was tiredness or indecision, but that was some slow movement by %(character)s."
            "%(character)s was moving slower than their usual pace of %(speed)d.",
            "Something has got into %(character)s, they're going pretty slowly for them.",
            "%(character)s was slowing down to give it some thought.",
            "That's slower movement than we usually see from %(character)s.",
            "I'm used to seeing %(character)s move a bit quicker.",
            "Sluggish movement from %(character)s.",
            "Think what %(character)s could do if they just moved a bit faster, like they normally do."
        ]

    def get_standard_tag_line(self):
        return random.choice(self.standard_tag_lines)
        
    def get_fast_tagger_slow_tagged_line(self):
        return random.choice(self.fast_tagger_slow_tagged_lines)
        
    def get_fast_tagger_line(self):
        return random.choice(self.fast_tagger_lines)
        
    def get_slow_tagged_line(self):
        return random.choice(self.slow_tagged_lines)
        
    def get_number_of_tags_line(self):
        return random.choice(self.number_of_tags_lines)
        
    def get_average_speed_line(self):
        return random.choice(self.average_speed_lines)
        
    def get_faster_than_average_line(self):
        return random.choice(self.faster_than_average_lines)
        
    def get_slower_than_average_line(self):
        return random.choice(self.slower_than_average_lines)
