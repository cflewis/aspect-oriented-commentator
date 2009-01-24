# Source code distributed under the Copyright (c) 2008, Chris Lewis
# Authors: Chris Lewis (http://work.chris.to), John David Funge (www.jfunge.com)
#
# Licensed under the Academic Free License version 3.0 
# (for details see LICENSE.txt in this directory).

import pygame

# time is measured in milliseconds
ticksPerSec = 1000.0

def getTime():
    return pygame.time.get_ticks()/ticksPerSec
