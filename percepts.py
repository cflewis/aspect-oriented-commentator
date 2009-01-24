# Source code distributed under the Copyright (c) 2008, Chris Lewis
# Authors: Chris Lewis (http://work.chris.to), John David Funge (www.jfunge.com)
#
# Licensed under the Academic Free License version 3.0 
# (for details see LICENSE.txt in this directory).

import timer
import character
import util
import vec
import gui

from numpy import *

class Percepts:

    def __init__(self, gs):
        self.gs = gs
        self.me = None

        self.p = zeros((util.numDim,), float)
        self.cp = zeros((util.numDim,), float)
        self.rp = zeros((util.numDim,), float)
        self.ip = zeros((util.numDim,), float)

    def getMe(self):
        return self.me

    # Set the character from whose point of view percepts are to be calculated.
    # This method should be called prior to the associated character's brain
    # selecting an action.  Most percepts "pull" information from the game as it is
    # required by a controller.  The "setMe" method is the main "push" method for telling
    # a controller which character is selecting an action.
    def setMe(self, me):
        self.me = me
        self.nearestCharacter = None
        self.nextCollider = None

    # TODO: this probably shouldn't be independent of gs
    def getTime(self):
        return timer.getTime()

    def myPosition(self):
        return self.me.getPosition()

    def mySpeed(self):
        return self.me.getSpeed()

    def myOrientation(self):
        return self.me.getOrientation()

    def myVelocity(self):
        return self.me.getVelocity()

    def myMaxExtent(self):
        return self.me.getMaxExtent()

    def tagged(self):
        return self.gs.tagged == self.me

    def taggedPosition(self):
        return self.gs.tagged.getPosition()

    def taggedSpeed(self):
        return self.gs.tagged.getSpeed()

    def taggedOrientation(self):
        return self.gs.tagged.getOrientation()

    def myNearestCharacter(self):
        # If the previous calculation of nearestCharacter is still valid, return the
        # cached value.
        if not self.nearestCharacter:
            self.dMin = Inf
            for c in self.gs.characters:
                if self.me == c:
                    continue # Don't include me!

                # TODO: use squaredDistanceTo instead
                d = self.myDistanceTo(c)
                if d < self.dMin:
                    self.dMin = d
                    self.nearestCharacter = c

        return self.nearestCharacter

    def myNearestCharacterPosition(self):
        return self.myNearestCharacter().getPosition()

    def myNearestCharacterDistance(self):
        if not self.nearestCharacter:
            self.myNearestCharacter()

        return self.dMin

    def myNearestCharacterSpeed(self):
        return self.myNearestCharacter().getSpeed()

    def myNearestCharacterOrientation(self):
        return self.myNearestCharacter().getOrientation()

    def myDistanceTo(self, o):
        return self.me.distanceTo(o)

    def myDistanceToTagged(self):
        return self.me.distanceTo(self.gs.tagged)

    def myTimeToCollision(self):
        self.cp = self.myNextCollisionPoint()

        if Inf == vec.length(self.cp):
            return Inf # No collisions detected.

        # vec.copy(self.myPosition(), gui.debugPt0)
        # vec.copy(self.cp, gui.debugPt1)

        self.rp = self.cp - self.myPosition()

        # With the current set of assumptions, me could not be on a
        # collision course in the first place if the following assert
        # fails.
        assert 0 <= vec.dot(self.rp, self.myVelocity())

        # TODO: To more accurately compute the time to collision we should
        # take into account the velocity of the collider.  But if we do
        # that here, we should have done that in the computation of the
        # nearest collider.  For example, if a collider is moving out of
        # the way faster than we are approaching it, then there is no
        # danger of collision after all.  But remember this whole method
        # is a percept and percepts don't have to be perfect as they are
        # meant to model how the NPC thinks about the world.  And in that
        # vein, using a stationary snapshot of the world is OK for now.
        # Especially so as the snapshot is regularly updated when the
        # percept is recalculated every time an action is selected.
        # colliderVel = vec.dot(self.rp, self.nextCollider)
        # relVel = myVel - colliderVel;

        return vec.length(self.rp) # / self.myVelocity()

    def myNextCollisionPoint(self):
        if not self.nextCollider:
            self.myNextCollider()

        if not self.nextCollider:
            vec.set(Inf, self.cp)
            return self.cp

        # TODO: This was already calculated in myNextCollider
        return self.cp

    def myNextCollider(self):
        # If the previous calculation of the next collider is still valid,
        # return the cached value.

        if self.nextCollider:
            return self.nextCollider

        which = None
        dMin = Inf

        for o in self.gs.obstacles:
            if self.me == o:
                continue # Don't include me!

            self.ip = o.nearestIntersection(self.me, self.ip)

            # Infinity is used to indicate no intersection.
            if vec.length(self.ip) < Inf:
                p = self.ip - self.myPosition()

                d = vec.length(p) - self.myMaxExtent()
                if d < dMin:
                    dMin = d
                    which = o
                    vec.copy(self.ip, self.cp)

        # We must at least be on a collision course with one of the sides.
        # TODO: turn side collisions back on
        # if false and not which:
        #    print self.myPosition(), "; ", self.myOrientation()
        #    pause
        #    assert which

        # Computing the nearest collider is expensive so cache the result
        # in case it's needed again.

        # TODO: Could also be worth caching dMin as the distance to the
        # nearest collider.

        self.nextCollider = which
        return which

