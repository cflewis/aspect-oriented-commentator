# Source code distributed under the Copyright (c) 2008, Chris Lewis
# Authors: Chris Lewis (http://work.chris.to), John David Funge (www.jfunge.com)
#
# Licensed under the Academic Free License version 3.0 
# (for details see LICENSE.txt in this directory).

import util
import util2D
import vec
import percepts

from numpy import *
import math

class Action:

    def __init__(self):
        self.direction = zeros((util.numDim,), float)
        self.speed = 0.0
        self.tmp = zeros((util.numDim,), float)

    def setSpeed(self, speed):
        self.speed = speed

    def setDirection(self, direction):
        self.direction = direction

    def getDesiredAcceleration(self, maxSpeed):
        return vec.scale(self.direction, self.speed * maxSpeed, self.tmp)

class Brain:

    def __init__(self, percepts):
        self.percepts = percepts
        self.action = Action()

    def calcAction(self):
        assert False, "This is meant to be an abstract class"

    def getPercepts(self):
        return self.percepts

    def getAction(self):
        return self.action

class BrainPC(Brain):

    def __init__(self, percepts, inputDevice):
        Brain.__init__(self, percepts)
        self.inputDevice = inputDevice

    def calcAction(self):
        self.action.direction[0] = self.inputDevice.getX()
        self.action.direction[1] = self.inputDevice.getY()

        if vec.isAlmostZero(self.action.direction):
            vec.zeroize(self.action.direction) # TODO: necessary?
            self.action.speed = 0.0
        else:
            self.action.speed = min(1.0, vec.length(self.action.direction))
            vec.normalize(self.action.direction, self.action.direction)

class BrainWander(Brain):

    def calcAction(self):
        vec.normalize(vec.randomVec(self.action.direction), self.action.direction)
        self.action.speed = util.clamp(util.uniform(), 0.25, 1.0)

class BrainPeriodic(Brain):

    def __init__(self, percepts, brain, period):
        Brain.__init__(self, percepts)
        self.timeOfLastDecision = -1.0
        self.period = period
        self.brain = brain

    def calcAction(self):
        time = self.percepts.getTime()

        if 0 <= self.timeOfLastDecision and time - self.timeOfLastDecision < self.period:
            return

        self.timeOfLastDecision = time
        self.brain.calcAction()
        self.action = self.brain.action

class BrainPeriodicRamp(Brain):

    def __init__(self, percepts, distancePercept, brain, nearDistance, farDistance, minPeriod, maxPeriod):
        Brain.__init__(self, percepts)
        self.timeOfLastDecision = -1.0
        self.distancePercept = distancePercept
        self.brain = brain
        self.nearDistance = nearDistance
        self.farDistance = farDistance
        self.minPeriod = minPeriod
        self.maxPeriod = maxPeriod

    def calcAction(self):
        time = self.percepts.getTime()

        period = util.clamp(self.maxPeriod/self.farDistance * self.distancePercept(self.percepts), self.minPeriod, self.maxPeriod)

        # d = self.distancePercept(self.percepts)
        # slope = (self.maxPeriod - self.minPeriod)/(self.nearDistance - self.farDistance)
        # intercept = self.maxPeriod + self.nearDistance * slope
        # period = util.clamp(d * slope + intercept, self.minPeriod, self.maxPeriod)

        if 0 <= self.timeOfLastDecision and time - self.timeOfLastDecision < period:
            return

        self.timeOfLastDecision = time
        self.brain.calcAction()
        self.action = self.brain.action

class BrainRandomize(Brain):

    def __init__(self, percepts, brain, distancePercept, nearDistance, farDistance):
        Brain.__init__(self, percepts)
        self.brain = brain
        self.distancePercept = distancePercept
        self.nearDistance = nearDistance
        self.farDistance = farDistance
        self.tmp = zeros((util.numDim,), float)

    def calcAction(self):
        self.brain.calcAction()
        a = self.brain.action

        d = self.distancePercept(self.percepts)

        # Compute the distance as a fraction of "farDistance"
        dFrac = min(1.0, d/self.farDistance)

        angle = util2D.angle(a.direction) + dFrac + math.pi*random.random() - 0.5*math.pi
        self.action.setDirection(util2D.dir(angle, self.tmp))

        # TODO: pass in desired distribution (and associated parameters) to the constructor
        # Add more variance when the tagged character is far away, e.g.
        #
        # stdMax = 130
        # std = min(stdMax, stdMax * d/farDistance)
        #
        # v = utile2D.normalDir(util2D.angle(v), std)

        # TODO: consider randomizing speed too?  Or make separate randomizeDirection
        # and randomizeSpeed?

        assert 0 < a.speed
        self.action.setSpeed(a.speed)

class BrainConditional(Brain):

    def __init__(self, percepts, conditionPercept, brainTrue, brainFalse):
        Brain.__init__(self, percepts)
        self.brainTrue = brainTrue
        self.brainFalse = brainFalse
        self.conditionPercept = conditionPercept

    def calcAction(self):
        if self.conditionPercept(self.percepts):
            self.brainTrue.calcAction()
            self.action = self.brainTrue.action
            return

        self.action = self.brainFalse.calcAction()
        self.action = self.brainFalse.action

class BrainEvade(Brain):

    def __init__(self, percepts, targetPositionPercept):
        Brain.__init__(self, percepts)
        self.targetPositionPercept = targetPositionPercept
        self.tmp = zeros((util.numDim,), float)

    def calcAction(self):
        v = self.percepts.myPosition() - self.targetPositionPercept(self.percepts)

        # TODO: consider predicating on v.length() e.g. inversely proportional so
        # that speed increases as tagged character gets closer
        # max(0.0, min(1.0, 1.0 - (0.25*tagDist)/tagFar))
        self.action.setSpeed(1.0)
        self.action.setDirection(vec.normalize(v, self.tmp))

class BrainPursue(Brain):

    def __init__(self, percepts, targetPositionPercept):
        Brain.__init__(self, percepts)
        self.targetPositionPercept = targetPositionPercept
        self.tmp = zeros((util.numDim,), float)

    def calcAction(self):
        v = self.targetPositionPercept(self.percepts) - self.percepts.myPosition()

        # TODO: consider predicating speed on v.length()
        self.action.setSpeed(1.0)
        self.action.setDirection(vec.normalize(v, self.tmp))

class BrainAvoid(Brain):

    def __init__(self, percepts, defaultBrain):
        Brain.__init__(self, percepts)
        self.defaultBrain = defaultBrain
        self.rp = zeros((util.numDim,), float)
        self.tmp = zeros((util.numDim,), float)
        self.timeLastCollisionDetected = -1.0

    def calcAction(self):
        # TODO: make this settable
        soonThreshold = 50.0

        # TODO: consider re-factoring using BrainConditional (or something like it)
        # TODO: this is hardwired to only avoid static obstacles

        if soonThreshold < self.percepts.myTimeToCollision() or (self.percepts.myNextCollider() and Inf != self.percepts.nextCollider.mass):
             # No collision danger
             time = self.percepts.getTime()
             # How many milliseconds to wait after a potential collision was detected before
             # resuming with the default controller.  TODO: consider making a settable class variable.
             delay = 0.5
             if self.timeLastCollisionDetected < 0 or delay < time - self.timeLastCollisionDetected:
                 self.defaultBrain.calcAction()
                 self.action = self.defaultBrain.action
             else:
                 # Just continue with last action.
                 # TODO: consider some time discounted blend of default controller and
                 # avoidance vector.
                 pass

             return

        self.timeLastCollisionDetected = self.percepts.getTime()

        # Collision danger present so need to take evasive action.
        self.rp = vec.normalize(self.percepts.myNextCollisionPoint() - self.percepts.myPosition(), self.rp)

        self.tmp = util2D.perpendicularTo(self.rp, self.percepts.myNextCollider().normalTo(self.percepts.getMe(), self.tmp), self.tmp)[0]

        assert util.isAlmostZero(vec.dot(self.rp, self.tmp))

        self.action.setDirection(self.tmp)
        # TODO: modulate the speed based on time until collision and whatever the defaultControler
        # set it to.
        self.action.setSpeed(1.0)
