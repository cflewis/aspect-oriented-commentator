# Source code distributed under the Copyright (c) 2008, Chris Lewis
# Authors: Chris Lewis (http://work.chris.to), John David Funge (www.jfunge.com)
#
# Licensed under the Academic Free License version 3.0 
# (for details see LICENSE.txt in this directory).

import gui
import timer
import vec
import util

import math
import pygame

from numpy import *

class Renderer:

    def __init__(self, foregroundName, flashColorName):
        self.foregroundName = foregroundName
        self.flashColorName = flashColorName

        self.foreground = pygame.color.Color(self.foregroundName)
        self.flashColor = pygame.color.Color(self.flashColorName)

        self.alt = False
        self.flash = False

    def flashOn(self):
        self.flash = True

    def flashOff(self):
        self.flash = False

    def altOn(self):
        self.alt = True

    def altOff(self):
        self.alt = False

    def render(self):
        if self.flash and math.fmod(timer.getTime(), 2.0) < 1.0:
            gui.setColor(self.flashColor)
        else:
            gui.setColor(self.foreground)

class RendererCircle(Renderer):

    def render(self, o):
        Renderer.render(self)

        gui.drawCircle(o.getPosition(), o.getOrientation(), o.getShape().getRadius())

class RendererCharacter(RendererCircle):

    def __init__(self, foregroundName, flashColorName):
        Renderer.__init__(self, foregroundName, flashColorName)
        self.tmp = zeros((util.numDim,), float)

    def render(self, c):
        RendererCircle.render(self, c)

        start = c.getPosition() + vec.scale(c.getOrientation(), c.shape.radius, self.tmp)
        gui.drawArrow(start, c.getOrientation(), 1.5 * c.shape.getRadius() * (c.getSpeed()/c.maxSpeed))

