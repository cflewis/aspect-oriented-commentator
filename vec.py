# Source code distributed under the Copyright (c) 2008, Chris Lewis
# Authors: Chris Lewis (http://work.chris.to), John David Funge (www.jfunge.com)
#
# Licensed under the Academic Free License version 3.0 
# (for details see LICENSE.txt in this directory).

import util

from numpy import *

def set(x, u):
    for i in range(len(u)):
        u[i] = x

    return u

def scale(u, x, v):
    multiply(u, x, v)

    return v

def normalize(u, v):
    l = length(u)
    if (util.isAlmostZero(l)):
        zeroize(v)
    else:
        scale(u, 1.0/l, v)

    return v

def length(u):
    return linalg.linalg.norm(u)

def lengthSq(u):
    s = 0.0
    for x in u:
        s += x * x

    return s

def randomVec1(u, v, w):
    multiply(random.random(len(u)), u, w)

    return w

def randomVec(u):
    return random.random(u.shape)

def zeroize(u):
    return set(0.0, u)

def copy(u, v):
    for i in range(len(u)):
        v[i] = u[i]

    return v

def clampMaxLength(u, x, v):
    l = length(u)

    if l < x:
        copy(u, v)
    elif util.isAlmostZero(l):
        zeroize(v)
    else:
        scale(u, x/l, v)

    return v

def wrap(u, v, w):
    copy(u, w)

    for i in range(len(w)):
        assert 0 < v[i], "infinite loop"

        while w[i] < 0:
           w[i] += v[i]

        while v[i] < w[i]:
           w[i] -= v[i]

    return w

def relativeTo(u, v, w):
    for i in range(len(u)):
        w[i] = v[i] - u[i]

    return w

def isAlmostZero(u):
    for x in u:
        if not util.isAlmostZero(x):
            return False

    return True
