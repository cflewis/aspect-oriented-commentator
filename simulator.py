# Source code distributed under the Copyright (c) 2008, Chris Lewis
# Authors: Chris Lewis (http://work.chris.to), John David Funge (www.jfunge.com)
#
# Licensed under the Academic Free License version 3.0 
# (for details see LICENSE.txt in this directory).

import util2D
import timer
import vec
import util

from numpy import *

class Simulator:
    def __init__(self, gs):
        self.gs = gs
        self.t = zeros((util.numDim,), float)
        self.n = zeros((util.numDim,), float)
        self.nTmp = zeros((util.numDim,), float)
        self.vt = zeros((util.numDim,), float)
        self.vn = zeros((util.numDim,), float)

    def calcActions(self):
        for c in self.gs.characters:
            c.getController().getPercepts().setMe(c)
            c.calcAction()

    def processActions(self, deltaT):
        for c in self.gs.characters:
            # calculate character's required acceleration for the desired velocity
            acceleration = c.getAction().getDesiredAcceleration(c.maxSpeed) - c.getVelocity()
            # calculate required force from the acceleration
            force = vec.clampMaxLength(vec.scale(acceleration, c.mass, self.n), c.maxForce, self.t)
            # re-calculate acceleration for new (possibly) clamped force
            c.setVelocity(vec.clampMaxLength(c.getVelocity() + vec.scale(force, deltaT/c.mass, self.n), c.maxSpeed, self.t))

    def resolveCollisions(self):
        e = 0.75              # coefficient of restitution
        minTagInterval = 3.0  # minimum time allowed between re-tagging

        now = timer.getTime()
        loopCount = 0

        while True:
            isCollision = False

            for i in self.gs.characters:
                for j in self.gs.characters:

                    if i == j:
                        continue
  
                    if not i.isColliding(j):
                        continue

                    isCollision = True

                    # We have to keep computing these in case they changed in a previous collision
                    uc = i.getVelocity()
                    mc = i.mass

                    self.t = i.normalTo(j, self.t)
                    self.n = util2D.perpendicularTo(self.t, self.n, self.nTmp)[0]

                    uct = dot(uc, self.t)
                    ucn = dot(uc, self.n)

                    mo = j.mass

                    uo = j.getVelocity()

                    uot = dot(uo, self.t)
                    uon = dot(uo, self.n)

                    k = (uct - uot)/(mc + mo)
                    vct = uct - (1 + e) * mo * k
                    vot = uot + (1 + e) * mc * k

                    i.setVelocity(vec.scale(self.t, vct, self.vt) + vec.scale(self.n, ucn, self.vn))

                    j.setVelocity(vec.scale(self.t, vot, self.vt) + vec.scale(self.n, uon, self.vn))

                    # TODO: limit re-tagging restriction to previously tagged character only
                    if j.tagged and minTagInterval < now - self.gs.lastTagTime:
                        self.gs.setTagged(i, j, now)
                    elif i.tagged and minTagInterval < now - self.gs.lastTagTime:
                        self.gs.setTagged(j, i, now)

                for j in self.gs.nonCharacterObstacles:
                    if not i.isColliding(j):
                        continue

                    isCollision = True

                    uc = i.getVelocity()

                    self.t = i.normalTo(j, self.t)
                    self.n = util2D.perpendicularTo(self.t, self.n, self.nTmp)[0]

                    uct = dot(uc, self.t)
                    ucn = dot(uc, self.n)

                    vct = -e * uct
                    i.setVelocity(vec.scale(self.t, vct, self.vt) + vec.scale(self.n, ucn, self.vn))

            if not isCollision:
                break

            assert loopCount < 1000, "something probably went wrong"
            loopCount += 1

    def updateGameState(self, deltaT):
        for c in self.gs.characters:
            c.setPosition(vec.wrap(c.getPosition() + vec.scale(c.getVelocity(), deltaT, self.t), self.gs.worldDim, self.n))
            c.setActualVelocity(c.getVelocity())

    def forward(self, deltaT):
        self.calcActions()
        self.processActions(deltaT)
        self.resolveCollisions()
        self.updateGameState(deltaT)


