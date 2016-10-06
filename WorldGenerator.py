import math
import random


def createGrid(size):
    caves = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append('_')
        caves.append(row)
    return caves


def addObstacles(caves, oProbs):
    numObs = round(len(caves) * len(caves) * oProbs)
    for i in range(numObs):
        rcol = random.randint(0, len(caves) - 1)
        rrow = random.randint(0, len(caves) - 1)
        while caves[rcol][rrow] != '_' or (rcol == 0 and rrow == 0):
            rcol = random.randint(1, len(caves))
            rrow = random.randint(1, len(caves))
        caves[rcol][rrow] = 'o'
    return caves


def addPits(caves, pProbs):
    numPits = round(len(caves) * len(caves) * pProbs)
    for i in range(numPits):
        rcol = random.randint(0, len(caves) - 1)
        rrow = random.randint(0, len(caves) - 1)
        while caves[rcol][rrow] != '_' or (rcol == 0 and rrow == 0):
            rcol = random.randint(1, len(caves))
            rrow = random.randint(1, len(caves))
        caves[rcol][rrow] = 'p'
    return caves


def addWumpus(caves, wProbs):
    numWumpi = round(len(caves) * len(caves) * wProbs)
    for i in range(numWumpi):
        rcol = random.randint(0, len(caves) - 1)
        rrow = random.randint(0, len(caves) - 1)
        while caves[rcol][rrow] != '_' or (rcol == 0 and rrow == 0):
            rcol = random.randint(1, len(caves))
            rrow = random.randint(1, len(caves))
        caves[rcol][rrow] = 'w'
    return caves


def addGold(caves):
    rcol = random.randint(0, len(caves) - 1)
    rrow = random.randint(0, len(caves) - 1)
    while caves[rcol][rrow] != '_' or (rcol == 0 and rrow == 0):
        rcol = random.randint(1, len(caves))
        rrow = random.randint(1, len(caves))
    caves[rcol][rrow] = 'g'
    return caves


def createWorld(size, oProbs, pProbs, wProbs):
    world = createGrid(size)
    world = addObstacles(world, oProbs)
    world = addPits(world, pProbs)
    world = addWumpus(world, wProbs)
    world = addGold(world)
    return world

