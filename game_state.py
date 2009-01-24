# Source code distributed under the Copyright (c) 2008, Chris Lewis
# Authors: Chris Lewis (http://work.chris.to), John David Funge (www.jfunge.com)
#
# Licensed under the Academic Free License version 3.0 
# (for details see LICENSE.txt in this directory).

import timer

class GameState:
    def __init__(self, worldDim):
        self.obstacles = []
        self.characters = [] 
        self.nonCharacterObstacles = []
        self.tagged = None
        self.worldDim = worldDim
        self.frame = 0
        self.lastTagTime = 0

    def setTagged(self, newTagged, oldTagged, time):
        newTagged.tag()
        if oldTagged:
            oldTagged.untag()
        assert self.tagged == oldTagged, "game got confused about who was tagged"
        self.tagged = newTagged

        self.lastTagTime = time

    def addCharacter(self, c):
        if not self.tagged:
           self.setTagged(c, None, timer.getTime())

        self.characters.append(c)

    def addObstacle(self, o):
        self.obstacles.append(o)

        self.nonCharacterObstacles.append(o)

    def incFrame(self):
        self.frame += 1

    def render(self):
        for i in self.obstacles:
            i.render()

        for i in self.characters:
            i.render()

