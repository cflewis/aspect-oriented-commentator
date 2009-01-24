# Source code distributed under the Copyright (c) 2008, Chris Lewis
# Authors: Chris Lewis (http://work.chris.to), John David Funge (www.jfunge.com)
#
# Licensed under the Academic Free License version 3.0 
# (for details see LICENSE.txt in this directory).

import math

from numpy import random

numDim = 2

def clamp(x, l=0.0, u=1.0):
    return max(l, min(x, u))

def uniform():
    return random.random()

def radToDeg(x):
    return x * 180.0/math.pi

def degToRad(x):
    return x * math.pi/180.0

def isAlmostEq(x, y):
    eps = 0.0001
    return math.fabs(x - y) < eps

def isAlmostZero(x):
    return isAlmostEq(x, 0.0)

