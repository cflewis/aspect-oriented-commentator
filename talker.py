#!/usr/bin/env python
# encoding: utf-8
"""
talker.py

Created by Chris Lewis on 2008-11-26.
Copyright (c) 2008 Chris Lewis. All rights reserved.
"""

import time
import threading
import os
import sys

class Talker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.finished = threading.Event()
        self.waiting_comments = []
        
    def run(self):
        while not self.finished.isSet():
            if len(self.waiting_comments) > 0:
                self.say(self.waiting_comments.pop(0))
                
                # cflewis | 2008-11-26 | Sleep longer than waiting for
                # a comment to prevent over-output
                self.finished.wait(2)
            else:
                self.finished.wait(1)
    
    def addComment(self, comment):
        # cflewis | 2008-11-26 | Pop off comments that are too old.
        # They won't be getting said
        while len(self.waiting_comments) > 1:
            self.waiting_comments.pop(0)
            
        self.waiting_comments.append(comment)
    
    def say(self, comment):
        if sys.platform == "darwin":
            os.system('say "' + comment +' "')
        
    def end(self):
        self.finished.set()
        self.join()

if __name__ == '__main__':
    unittest.main()