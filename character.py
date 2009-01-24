# Source code distributed under the Copyright (c) 2008, Chris Lewis
# Authors: Chris Lewis (http://work.chris.to), John David Funge (www.jfunge.com)
#
# Licensed under the Academic Free License version 3.0 
# (for details see LICENSE.txt in this directory).

import util
import vec

import mm

import pygame
import math

from numpy import *

class Shape:

    def __init__(self):
        self.orientation = zeros((util.numDim,), float)
        self.orientation[0] = 1.0
        self.position = zeros((util.numDim,), float)

    def setPosition(self, position):
        vec.copy(position, self.position)

    def setOrientation(self, orientation):
        assert util.isAlmostEq(1.0, vec.length(orientation)), 'invalid orientation ' + str(orientation)

        vec.copy(orientation, self.orientation)

class Circle(Shape):

    def __init__(self, radius):
        Shape.__init__(self)
        self.radius = radius

    def getRadius(self):
        return self.radius

    def getMaxExtent(self):
        return self.radius

@mm.multimethod(Circle, Circle, ndarray)
def normalTo(c0, c1, n):
    return vec.normalize(c1.position - c0.position, n)

@mm.multimethod(Circle, Circle)
def distanceTo(c0, c1):
   return vec.length(c0.position - c1.position) - c0.radius - c1.radius

@mm.multimethod(Circle, Circle)
def isTouching(c0, c1):
   return vec.lengthSq(c0.position - c1.position) <= (c0.radius + c1.radius)*(c1.radius + c1.radius)

@mm.multimethod(Circle, Circle, ndarray)
def nearestIntersection(c0, c1, q):
    p = c1.position
    v = c1.orientation

    rp = p - c0.position
    k0 = vec.lengthSq(rp) - c0.getRadius() * c0.getRadius()
    k1 = vec.dot(v, rp)

    roots = []
    k = k1 * k1 - k0
    if util.isAlmostZero(k):
        roots.append(-k1)
    elif 0.0 < k:
        kSqrt = math.sqrt(k)
        roots.append(-k1 - kSqrt)
        roots.append(-k1 + kSqrt)
        assert roots[0] < roots[1]

    vec.set(Inf, q)

    for root in roots:
        if util.isAlmostZero(root) or 0 < root:
            q = vec.scale(v, root, q)
            q = q + p
            break

    return q

class Obstacle:

    def __init__(self, shape):
        self.shape = shape
        self.speed = 0.0
        self.rndr = None
        self.mass = Inf
        self.velocity = zeros((util.numDim,), float)
        self.tmp = zeros((util.numDim,), float)
        self.actualVelocity = None
        self.actualSpeed = 0.0

    def getShape(self):
        return self.shape

    def setRenderer(self, rndr):
        self.rndr = rndr

    def render(self):
        if self.rndr:
            self.rndr.render(self)

    def normalTo(self, o, n):
        return normalTo(self.shape, o.shape, n)

    def getPosition(self):
        return self.shape.position

    def getOrientation(self):
        assert util.isAlmostEq(1.0, vec.length(self.shape.orientation)), 'invalid orientation ' + str(self.shape.orientation)

        return self.shape.orientation

    def getMaxExtent(self):
        return self.shape.getMaxExtent()

    def setPosition(self, position):
        self.shape.setPosition(position)

    def setVelocity(self, velocity):
        s = vec.length(velocity)
        if util.isAlmostZero(s):
            self.setSpeed(0)
            # Don't change the orientation if the speed is zero.
        else:
            self.setSpeed(s)
            self.shape.setOrientation(vec.normalize(velocity, self.velocity))

    def getVelocity(self):
        # TODO: cache to avoid recomputing
        return vec.scale(self.shape.orientation, self.speed, self.velocity)

    def setSpeed(self, speed):
        self.speed = speed

    def getSpeed(self):
        return self.speed

    def isTouching(self, o):
        return isTouching(self.shape, o.shape)

    def isColliding(self, o):
        v0 = self.getVelocity()
        v1 = o.getVelocity()
        self.tmp = self.normalTo(o, self.tmp)

        return self.isTouching(o) and dot(v0, self.tmp) > dot(v1, self.tmp)

    def distanceTo(self, o):
        return distanceTo(self.shape, o.shape)

    def nearestIntersection(self, o, p):
        return nearestIntersection(self.shape, o.shape, p)
        
    def setActualVelocity(self, velocity):
        self.actualVelocity = velocity
        self.actualSpeed = vec.length(velocity)
        
    def getActualVelocity(self):
        return self.actualVelocity
        
    def getActualSpeed(self):
        return self.actualSpeed

class Character(Obstacle):

    def __init__(self, shape, brain):
        Obstacle.__init__(self, shape)
        self.brain = brain
        self.tagged = False
        self.maxSpeed = 100.0
        self.mass = 1.0
        self.maxForce = 150.0
        self.name = "The NPC With No Name"

    def tag(self):
        self.tagged = True

    def untag(self):
        self.tagged = False

    def render(self):
        if self.tagged and self.rndr:
            self.rndr.flashOn()
        else:
            self.rndr.flashOff()

        Obstacle.render(self)

    def getController(self):
        return self.brain

    def calcAction(self):
        self.brain.calcAction()

    def getAction(self):
        return self.brain.getAction()
        
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name

