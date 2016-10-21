import random

def createGrid(size):
    """creates an empty square grid (2d array) that will be populated using other methods"""
    #declare array
    caves = []

    for i in range(size):
        #declare and fill row where each row is an array
        row = []
        for j in range(size):
            row.append('_')
        #add row to the array
        caves.append(row)
    return caves


def addObstacles(caves, oProbs):
    """Adds obstacles to the 2d grid"""
    #calculate the number of obstacles present in the world
    numObs = round(len(caves) * len(caves) * oProbs)
    #add the obstacles
    for i in range(numObs):
        #generate random x and y location for obstacle
        rcol = random.randint(0, len(caves) - 1)
        rrow = random.randint(0, len(caves) - 1)
        #While the location is full, keep generating random numbers
        count = 0
        while caves[rcol][rrow] != '_' or (rcol == 0 and rrow == 0) or count <= len(caves) ** 3:
            rcol = random.randint(0, len(caves)-1)
            rrow = random.randint(0, len(caves)-1)
            count += 1
        #Change _ to o
        caves[rcol][rrow] = 'o'
    return caves

def addPits(caves, pProbs):
    """Adds pits to the 2d grid"""
    # calculate the number of pits present in the world
    numPits = round(len(caves) * len(caves) * pProbs)
    # add the pits
    for i in range(numPits):
        #generate random x and y locations for the pit
        rcol = random.randint(0, len(caves) - 1)
        rrow = random.randint(0, len(caves) - 1)
        # While the location is full, keep generating random numbers
        count = 0
        while caves[rcol][rrow] != '_' or (rcol == 0 and rrow == 0)or count <= len(caves) ** 3:
            rcol = random.randint(0, len(caves)-1)
            rrow = random.randint(0, len(caves)-1)
            count += 1
        #Change _ to 'p'
        caves[rcol][rrow] = 'p'
    return caves

def addWumpus(caves, wProbs):
    """Adds wumpi to the 2d grid"""
    # calculate the number of wumpi present in the world
    numWumpi = round(len(caves) * len(caves) * wProbs)
    #add wumpi
    for i in range(numWumpi):
        rcol = random.randint(0, len(caves) - 1)
        rrow = random.randint(0, len(caves) - 1)
        # While the location is full, keep generating random numbers
        count = 0
        while caves[rcol][rrow] != '_' or (rcol == 0 and rrow == 0)or count <= len(caves) ** 3:
            rcol = random.randint(0, len(caves)-1)
            rrow = random.randint(0, len(caves)-1)
            count += 1
        #Change _ to 'w'
        caves[rcol][rrow] = 'w'
    return caves, numWumpi

def addGold(caves):
    rcol = random.randint(0, len(caves) - 1)
    rrow = random.randint(0, len(caves) - 1)
    # While the location is full, keep generating random numbers
    count = 0
    while caves[rcol][rrow] != '_' or (rcol == 0 and rrow == 0)or count <= len(caves) ** 3:
            rcol = random.randint(0, len(caves)-1)
            rrow = random.randint(0, len(caves)-1)
            count += 1
    #change _ to money moneyyyyyyyyy
    caves[rcol][rrow] = '$'
    return caves

def createWorld(size, oProbs, pProbs, wProbs):
    #Calls createGrid
    world = createGrid(size)
    #Adds all the other stuff to the world
    world = addObstacles(world, oProbs)
    world = addPits(world, pProbs)
    world, numWumpii = addWumpus(world, wProbs)
    world = addGold(world)
    return world, numWumpii


def printGrid(grid):
    #print(" N ")
    #print("W E")
    #print(" S ")
    
    for row in grid:
        print(row)
    print()
    