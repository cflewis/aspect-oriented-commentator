# Source code distributed under the Copyright (c) 2008, Chris Lewis
# Authors: Chris Lewis (http://work.chris.to), John David Funge (www.jfunge.com)
#
# Licensed under the Academic Free License version 3.0 
# (for details see LICENSE.txt in this directory).

import util
import vec

import math
from numpy import *

def perpendicularTo(u, n0, n1):
    # TODO: add more asserts of this nature
    assert len(u) == 2, "expected Vec of length 2"
    n0[0] = u[1]
    n0[1] = -u[0]

    n1[0] = -u[1]
    n1[1] = u[0]

    return [n0, n1]

def dir(t, v):
    assert len(v) == 2, "expected Vec of length 2"

    v[0] = math.cos(t)
    v[1] = math.sin(t)

    return v

def angle(u):
    l = vec.length(u)

    if util.isAlmostZero(l):
       return 0.0

    assert util.isAlmostEq(vec.length(u), 1.0), "input must be normalized, not " + str(u)

    return math.atan2(u[1], u[0])

def rotationMatrix(angle, m):
    m[0][0] = cos(t)
    m[0][1] = -sin(t)
    m[1][0] = sint(t)
    m[1][1] = cost(t)

    return m
