#!/usr/bin/env python

# Source code distributed under the Copyright (c) 2008, Chris Lewis
# Authors: Chris Lewis (http://work.chris.to), John David Funge (www.jfunge.com)
#
# Licensed under the Academic Free License version 3.0 
# (for details see LICENSE.txt in this directory).

from game_state import GameState
from simulator import Simulator
from gui import Gui, Keyboard
from renderer import *
from brain import *
from percepts import Percepts
from character import *
from commentator import *

import pygame

import logging
from springpython.aop import *


class Constants:
    pass

def setupNPCBrain(which, percepts):
    if which == "wander":
        return BrainPeriodic(percepts, BrainWander(percepts), 1.0)
    else:
        # Define what counts as the tagged character being "near"
        near = 2.0 * Constants.radius

        # Define what counts as the tagged character being "far"
        far = 10.0 * near

        # What's the minimum time (in seconds) allowed between decisions
        minPeriod = 0.2

        # What's the maximum time (in seconds) allowed between decisions
        maxPeriod = 0.4

        return BrainConditional(
            percepts,
            Percepts.tagged,
            BrainAvoid(
                percepts,
                BrainPursue(percepts, Percepts.myNearestCharacterPosition)),
            BrainAvoid(
                percepts,
                BrainPeriodicRamp(
                    percepts,
                    Percepts.myDistanceToTagged,
                    BrainRandomize(
                        percepts,
                        BrainEvade(percepts, Percepts.taggedPosition),
                        Percepts.myDistanceToTagged,
                        near,
                        far),
                    near,
                    far,
                    minPeriod,
                    maxPeriod)))
                    

def setupCharacters(gs, gui, kb):
    commentator = Commentator()
    #atexit.register(commentator.clean_up)
    rendererPC = RendererCharacter(Constants.pcColorName, Constants.flashColorName)

    percepts = Percepts(gs)

    tmp = zeros((util.numDim,), float)

    for i in range(Constants.numCharacters):
        brain = None
        if i == 0:
            brain = BrainPC(percepts, kb)
        else:
            brain = setupNPCBrain("ander", percepts)
        
        c = commentator.get_observed_character(Character(Circle(Constants.radius), brain))
        c.setPosition(vec.randomVec1(gs.worldDim, c.getPosition(), tmp))

        if i == 0:
            c.setRenderer(rendererPC)
            c.setName("Player")
        else:
            c.setName(Constants.npcNames[i - 1])
            rendererNPC = RendererCharacter(Constants.npcColors[i - 1], Constants.flashColorName)
            c.setRenderer(rendererNPC)
        gs.addCharacter(c)

def setupObstacles(gs, gui):
    r = RendererCircle(Constants.obstacleColorName, Constants.obstacleColorName)

    tmp = zeros((util.numDim,), float)

    for i in range(Constants.numObstacles):
        o = Obstacle(Circle(Constants.radius))
        o.setPosition(vec.randomVec1(gs.worldDim, o.getPosition(), tmp))
        o.setRenderer(r)
        gs.addObstacle(o)

def main(numFrames = -1):
    Constants.radius = 10.0
    Constants.numObstacles = 7
    Constants.numCharacters = 5
    Constants.worldDim = (512, 512)
    
    Constants.npcNames = ["Alice", "Bob", "Carol", "Dave"]
    
    # cflewis | 2008-11-02 | It would be nice to have a different colour,
    # but PyGame was only rendering this subset. Pretty annoying.
    Constants.npcColors = ["green", "red", "orange", "#ff00ff"]
    Constants.pcColorName = "blue"
    Constants.flashColorName = "white"
    Constants.backgroundName = "black"
    Constants.obstacleColorName = "white"

    commentator = Commentator()
    gs = commentator.get_observed_game_state(GameState(Constants.worldDim))
    gui = Gui(gs, Constants.backgroundName)

    sim = Simulator(gs)

    kb = Keyboard()

    setupCharacters(gs, gui, kb)

    setupObstacles(gs, gui)

    clock = pygame.time.Clock()

    while True:
        gui.render(gs)
        gs.incFrame()
        kb.processEvents()
        if kb.quit:
            break
        if 0 <= numFrames and numFrames <= gs.frame:
            break
        deltaT = clock.tick(30)/1000.0
        sim.forward(deltaT)

    gui.destroyWindow()

if __name__ == "__main__":
    logger = logging.getLogger("springpython")
    loggingLevel = logging.INFO
    logger.setLevel(loggingLevel)
    ch = logging.StreamHandler()
    ch.setLevel(loggingLevel)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") 
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    main()

# TODO:
# - more argument checking, especially for numbers that are supposed to be reals
# - minimize run-time object construction
# - port collisions with sides
# - enforce non-interpenetration constraint on starting position

