# Source code distributed under the Copyright (c) 2008, Chris Lewis
# Authors: Chris Lewis (http://work.chris.to), John David Funge (www.jfunge.com)
#
# Licensed under the Academic Free License version 3.0 
# (for details see LICENSE.txt in this directory).

import util
import util2D
import vec

from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import *
import pygame
import math

def setColor(color):
    glColor(color[0], color[1], color[2], color[3])

def drawCircle(center, orientation, radius):
    global quadric

    glPushMatrix()
    glTranslate(center[0], center[1], 0.0)
    glRotate(util.radToDeg(util2D.angle(orientation)), 0, 0, 1)
    gluPartialDisk(quadric, 0.0, radius, 20, 1, 0.0, 360.0)
    glPopMatrix()

def drawLine(begin, end):
    tmp = end - begin

    setColor(pygame.color.Color("red"))

    glPushMatrix()
    glTranslate(begin[0], begin[1], 0.0)

    glBegin(GL_LINE_STRIP)
    glVertex(0.0, 0.0)
    glVertex(tmp[0], tmp[1])
    glEnd()

    glPopMatrix()

def drawArrow(begin, lvec, lineSize):
    assert util.isAlmostEq(1.0, vec.length(lvec)), "unnormalized input"

    headSize = 0.5*lineSize
    lAngle = 2.5
    rAngle = -2.5

    # TODO: get rid of all these constructor calls
    hvec1 = zeros((util.numDim,), float)
    hvec2 = zeros((util.numDim,), float)
    tmp = zeros((util.numDim,), float)

    hvec1 = vec.scale(array([lvec[0]*math.cos(lAngle) - lvec[1]*math.sin(lAngle), lvec[0]*math.sin(lAngle) + lvec[1]*math.cos(lAngle)]), headSize, hvec1)
    hvec2 = vec.scale(array([lvec[0]*math.cos(rAngle) - lvec[1]*math.sin(rAngle), lvec[0]*math.sin(rAngle) + lvec[1]*math.cos(rAngle)]), headSize, hvec2)

    tmp = vec.scale(lvec, lineSize, tmp)

    rightWay = True
    glPushMatrix()
    if rightWay:
        glTranslate(begin[0], begin[1], 0.0)
    else:
        glTranslate(begin[0] - tmp[0], begin[1] - tmp[1], 0.0)

    glBegin(GL_LINE_STRIP)
    glVertex(0.0, 0.0)
    glVertex(tmp[0], tmp[1])
    glVertex(tmp[0] + hvec1[0], tmp[1] + hvec1[1])
    glEnd()
    glPopMatrix()

    glPushMatrix()
    if rightWay:
        glTranslate(begin[0] + tmp[0], begin[1] + tmp[1], 0.0)
    else:
        glTranslate(begin[0], begin[1], 0.0)

    glBegin(GL_LINES)
    glVertex(0.0, 0.0)
    glVertex(hvec2[0], hvec2[1])
    glEnd()
    glPopMatrix()

class Gui:

    def __init__(self, gs, backgroundName):
        pygame.init()

        display_flags = pygame.OPENGL|pygame.DOUBLEBUF

        if pygame.display.mode_ok(gs.worldDim, display_flags):
            self.screen = pygame.display.set_mode(gs.worldDim, display_flags)
        else:
            pass # TODO: quit with error

        global quadric

        quadric = gluNewQuadric()

        global debugPt0, debugPt1
        debugPt0 = zeros((util.numDim,), float)
        debugPt1 = zeros((util.numDim,), float)

        # self.resize(gs.worldDim)
        self.initGL(gs.worldDim, backgroundName)

    def resize(self, (width, height)):
        if height==0:
            height=1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0*width/height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def initGL(self, (width, height), backgroundName):

        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(0, width, 0, height, -2.0, 2.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glDepthFunc(GL_ALWAYS)
        glDisable(GL_LINE_STIPPLE)

        glShadeModel(GL_SMOOTH)
        c = pygame.color.Color(backgroundName)
        glClearColor(c[0], c[1], c[2], c[3])

    def render(self, gs):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        gs.render()

        global debugPt0, debugPt1
        drawLine( debugPt0, debugPt1 )

        pygame.display.flip()

    def destroyWindow(self):
        pass

class Keyboard:

    def __init__(self):
        self.keysStatus = { pygame.K_LEFT : False,
                            pygame.K_RIGHT: False,
                               pygame.K_UP: False,
                             pygame.K_DOWN: False }
        self.quit = False

    def processEvents(self):
        events = pygame.event.get()
   
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    self.keysStatus[event.key] = True

                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    self.quit = True

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    self.keysStatus[event.key] = False

            if event.type == pygame.QUIT:
                self.quit = True

    def getX(self):
        if self.keysStatus[pygame.K_LEFT]:
            return -1.0
        if self.keysStatus[pygame.K_RIGHT]:
            return 1.0

        return 0.0

    def getY(self):
        if self.keysStatus[pygame.K_UP]:
            return 1.0
        if self.keysStatus[pygame.K_DOWN]:
            return -1.0

        return 0.0

