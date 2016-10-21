import WorldGenerator as wg


# the explorer's knowledge base, reflects what it knows about the environment
class KnowledgeBase:
    def __init__(self, logger, size, oProbs, pProbs, wProbs, unknown_map):
        self.logger = logger
        # World will be sent in if loading from file, else create world
        if unknown_map == None:
            self.unknown_map, self.numWumpii = wg.createWorld(size, oProbs, pProbs, wProbs)
        else:
            self.unknown_map = unknown_map[0]
            self.numWumpii = unknown_map[1]

        # known_map is the one the Dudes see
        self.known_map = wg.createGrid(size)

        self.percepts = {} 
        self.facts = {}
        self.clause_list = []
        
        self.logger.info("Actual map")        
        wg.printGrid(self.logger, self.unknown_map)


    # Update the cell of the map dude's can see with char
    def update_cell(self, x, y, char):
        self.known_map[x][y] = char
        wg.printGrid(self.logger, self.known_map)

    # Update the cell of the real world with char
    def update_unknown_cell(self, x, y, char):
        self.unknown_map[x][y] = char

    # update the percepts according to the environment    
    def update_percept(self, x, y):
        percept_key = "{%d,%d}" % (x, y)    
        self.percepts.setdefault(percept_key,[])
        
        pCount = 0
        percept_glimmer = ''
        percept_breeze = ''
        percept_stench = '' 
        percept_thump = ''

        for value in self.percepts[percept_key]:
            pCount = len(value)
        
        # gold is in this cell, glimmer ($) is perceived, else (_) 
        if self.unknown_map[x][y] == '$':            
            self.logger.info("Explorer sees a glimmer in ({},{})".format(x,y))
            percept_glimmer = '$'
        else: 
            # no gold is perceived, update percept
            percept_glimmer = '_'
        
        # only adds the percept if it has not been added
        if (pCount == 0):
            # add the appropriate glimmer (gold) percept for this (x,y)
            self.percepts[percept_key].append(percept_glimmer)    
        
        # pit is in an adjacent cell, breeze (b) is perceived    
        # make sure is a valid choice for this x value
        if x < len(self.known_map) - 1:
            if self.unknown_map[x + 1][y] == 'p':    
                self.logger.info("Explorer feels a breeze in ({},{})".format(x,y))
                percept_breeze = 'b'
                self.set_potentials(x, y, 'd')
            if (x - 1) >= 0:        
                if self.unknown_map[x - 1][y] == 'p':    
                    self.logger.info("Explorer feels a breeze in ({},{})".format(x,y))
                    percept_breeze = 'b'
                    self.set_potentials(x, y, 'd')
        
        # make sure is a valid choice for this y value   
        if y < len(self.known_map) - 1:        
            if self.unknown_map[x][y + 1] == 'p':    
                self.logger.info("Explorer feels a breeze in ({},{})".format(x,y))
                percept_breeze = 'b'
                self.set_potentials(x, y, 'd')
                
            if y - 1 >= 0:          
                if self.unknown_map[x][y - 1] == 'p': 
                    self.logger.info("Explorer feels a breeze in ({},{})".format(x,y))
                    percept_breeze = 'b'
                    self.set_potentials(x, y, 'd')
        
        # no breeze perceived, update percept accordingly
        if ('b' not in percept_breeze):
            percept_breeze = '_'
        
        # add the appropriate breeze (pit) percept for this (x,y)
        if (pCount == 0):        
            self.percepts[percept_key].append(percept_breeze)            
        
        # wumpus is in an adjacent cell, stench (s) is perceived    
        # make sure is a valid choice for this x value
        if x < len(self.known_map) - 1:
            if self.unknown_map[x + 1][y] == 'w':    
                self.logger.info("Explorer smells a stench in ({},{})".format(x,y))
                percept_stench = 's'
                self.set_potentials(x, y, 'm')
        if (x - 1) >= 0:        
            if self.unknown_map[x - 1][y] == 'w':    
                self.logger.info("Explorer smells a stench in ({},{})".format(x,y))
                percept_stench = 's'
                self.set_potentials(x, y, 'm')
        
        # make sure is a valid choice for this y value   
        if y < len(self.known_map) - 1:        
            if self.unknown_map[x][y + 1] == 'w':    
                self.logger.info("Explorer smells a stench in ({},{})".format(x,y))
                percept_stench = 's'
                self.set_potentials(x, y, 'm')
                
            if y - 1 >= 0:          
                if self.unknown_map[x][y - 1] == 'w': 
                    self.logger.info("Explorer smells a stench in ({},{})".format(x,y))
                    percept_stench = 's'
                    self.set_potentials(x, y, 'm')
        
        # no stench perceived, update percept accordingly
        if ('s' not in percept_stench):
            percept_stench = '_'
        
        # add the appropriate stench (wumpus) percept for this (x,y)
        if (pCount == 0):        
            self.percepts[percept_key].append(percept_stench)  

        # obstacle is in this cell, thump (t) is perceived, else (_) 
        if self.unknown_map[x][y] == 'o':            
            self.logger.info("Explorer feels a thump in ({},{})".format(x,y))
            percept_thump = 't'
        else: 
            # no obstacle is perceived, update percept
            percept_thump = '_'

        # add the appropriate stench (wumpus) percept for this (x,y)
        if (pCount == 0):        
            self.percepts[percept_key].append(percept_thump)  

        self.logger.info("########Explorer's Percepts:")
        for key, value in self.percepts.items():
            x = '['
            for v in value:
                x += v
                x += ', '
            x += ']'
            self.logger.info(key + ':' + x)
        self.logger.info("############################")
        self.logger.info("")

        # take the information gathered from percepts, add it to the knowledge base
        # for value in self.percepts[percept_key]:
        #     if value != '_':
        #         self.tell(value, x, y)
        # return latest percept
        return self.percepts[percept_key]

    # if a breeze or stench is sensed, update neighbors to reflect potential danger
    def set_potentials(self, x, y, char):
        dont_overwrite = ['s', 'o', 'p', 'w']
        if x > 0:
            if self.known_map[x-1][y] not in dont_overwrite:
                self.update_cell(x-1, y, char)
        if x < len(self.known_map) - 1:
            if self.known_map[x + 1][y] not in dont_overwrite:
                self.update_cell(x+1, y, char)

        if y < len(self.known_map) - 1:
            if self.known_map[x][y+1] not in dont_overwrite:
                self.update_cell(x, y +1, char)

        if y > 0:
            if self.known_map[x][y -1] not in dont_overwrite:
                self.update_cell(x, y-1, char)

    # update the knowledge base with information gathered from percept
    def tell(self, assertion, x, y):
        key = "{%s,%s}" % (x, y)
        self.facts.setdefault(key,[])
        
        # for percept information, builds the appropriate assertion
        if assertion == '$':
            assertion = "GLIMMER({},{})".format(x,y)
        elif assertion == 'b':
            assertion = "BREEZE({},{})".format(x,y)
        elif assertion == 's':
            assertion = "STENCH({},{})".format(x,y)
        elif assertion == 't':
            assertion = "BUMP({},{})".format(x,y)
        elif assertion == 'a':
            assertion = "SAFE({},{})".format(x, y)
        elif assertion == 'o':
            assertion = "OBSTACLE({},{})".format(x, y)
        elif assertion == 'w':
            assertion = "WUMPUS({},{})".format(x, y)
        elif assertion == 'p':
            assertion = "PIT({},{})".format(x, y)

       # check that this rule is not already in dictionary
        if (assertion not in self.facts[key]):
            self.facts[key].append(assertion)
            # TODO unify and resolve to see if new facts come out

        self.logger.info("########Information in Knowledge Base:")
        for key, value in self.facts.items():
            x = '['
            for v in value:
                x += v
                x += ', '
            x += ']'
            self.logger.info(key + ':' + x)
            self.logger.info("##################################")
        self.logger.info("")

    # see if query is in Knowledge Base
    def ask(self, query):
        if query in self.facts:
            return True
        else:
            return False

    def clauses(self):
        """Creates and returns a list of clauses in the knowledge base.
        All Predicates with all caps, Instantiated variables with single capital letter at beginning,
        Uninstantiated variables lowercase char (cannot include v since v means or)
        All sentences in clause form
        Possble Actions: GRAB, TURN90, MOVEFORWARD, SHOOTARROW
        Possible Predicates: SAFE(x,y), BREEZE(x,y), STENCH(x,y), BUMP(x,y), PIT(x,y), WUMPUS(x,y), OBSTACLE(x,y),
        GOLD(x,y), AT(x,y)(?), FACING(d)
        """

        self.clause_list.append("!(BUMP(x,y)) v (OBSTACLE(x,y))") #If there's a bump, there must be an obstacle
        self.clause_list.append("(SAFE(x,y)) v (PIT(x,y)) v (WUMPUS(x,y)) v !(SAFE(x,y)) v !(PIT(x,y))") #If it's safe there are no pits or wumpi
        self.clause_list.append("(SAFE(x,y) v (PIT(x,y)) v (WUMPUS(x,y)) v !(SAFE(x,y)) v !(WUMPUS(x,y))")

        self.clause_list.append("!(POSSPIT(x,y)) v !(SAFE(x,y)) v !(PIT(x,y))") #A Possible Pit that is already safe means there is no pit there
        self.clause_list.append("!(POSSWUMP(x,y)) v !(SAFE(x,y)) v !(WUMPUS(x,y))")#A Possible Wumpus that is already safe means there is no wumpus there
        self.clause_list.append("!(PIT(x,y)) v !(SAFE(x,y))")
        self.clause_list.append("!(PIT(x,y)) v !(WUMPUS(x,y))") #Pits, wumpi and safe can not be in the same cells
        self.clause_list.append("!(WUMPUS(x,y)) v !(SAFE(x,y))")
        self.clause_list.append("!(WUMPUS(x,y)) v  !(PIT(x,y))")

        self.clause_list.append("!(BREEZE(x,y)) v (POSSPIT(x+1,y))")
        self.clause_list.append("!(BREEZE(x,y)) v (POSSPIT(x-1,y))")
        self.clause_list.append("!(BREEZE(x,y)) v (POSSPIT(x,y+1))")
        self.clause_list.append("!(BREEZE(x,y)) v (POSSPIT(x,y-1))")

        self.clause_list.append("!(STENCH(x,y)) v (POSSWUMP(x+1,y))")
        self.clause_list.append("!(STENCH(x,y)) v (POSSWUMP(x-1,y))")
        self.clause_list.append("!(STENCH(x,y)) v (POSSWUMP(x,y+1))")
        self.clause_list.append("!(STENCH(x,y)) v (POSSWUMP(x,y-1))")

        self.clause_list.append("(MOVE(x,y)) v !(SAFE(x,y)) v !(MOVE(x,y)) v (SAFE(x,y))")
        self.clause_list.append("(GRABGOLD(x,y)) v !(GLIMMER(x,y)) v !(GRABGOLD(x,y)) v (GLIMMER(x,y))")
        self.clause_list.append("(SHOOTARROW(x,y)) <=> (WUMPUS(x,y))")
        self.clause_list.append("(SHOOTARROW(x,y)) v !(WUMPUS(x,y)) v !(SHOOTARROW(x,y)) v (WUMPUS(x,y))")
        self.clause_list.append("(TURNL90(x,y)) <=> (PIT(x,y)) v (OBSTACLE(x,y)) v ")

        self.clause_list.append("FACING(NORTH) <=> (TURNL90(x,y) ^ FACING(EAST)) v (TURNR90(x,y) ^ FACING(WEST)")

        #self.clause_list.append("!BUMP(X,Y) v (OBSTACLE(X,Y))") #If there's a bump, there must be an obstacle
        #self.clause_list.append("SAFE(X,Y) <=> !(PIT(X,Y)) ^ !(WUMPUS(X,Y)") #If it's safe there are no pits or wumpi
        #self.clause_list.append("BREEZE(X,Y) <=> (PIT(X+1,Y) v PIT(X-1,Y) v PIT(X,Y+1) v PIT(X,Y-1))") #A breeze means there must be a pit in one of the surrounding cells
        #self.clause_list.append("STENCH(X,Y) <=> (WUMPUS(X+1,Y) v WUMPUS(X-1,Y) v WUMPUS(X,Y+1) v WUMPUS(X,Y-1))") #A stench means there must be a wumpus in one of the surrounding cells
        #self.clause_list.append("!POSSPIT(X,Y) v !SAFE(X,Y) v !PIT(X,Y)") #A Possible Pit that is already safe means there is no pit there
        #self.clause_list.append("!POSSWUMP(X,Y) v !SAFE(X,Y) v !WUMPUS(X,Y)")#A Possible Wumpus that is already safe means there is no wumpus there
        #self.clause_list.append("!PIT(X,Y) v (!SAFE(X,Y) ^ !WUMPUS(X,Y))") #Pits, wumpi and safe can not be in the same cells
        #self.clause_list.append("!WUMPUS(X,Y) v !SAFE(X,Y) ^ !PIT(X,Y)")
        #self.clause_list.append("!BREEZE(X,Y) v (POSSPIT(X+1,Y) ^ POSSPIT(X-1,Y) ^ POSSPIT(X,Y+1) ^ POSSPIT(X,Y-1))")
        #self.clause_list.append("!STENCH(X,Y) v (POSSWUMP(X+1,Y) ^ POSSWUMP(X-1,Y) ^ POSSWUMP(X,Y+1) ^ POSSWUMP(X,Y-1))")

        # FOR TESTING
        #self.clause_list.append("MOTHER(Lulu,Fifi)")
        #self.clause_list.append("ALIVE(Lulu)")
        #self.clause_list.append("!(MOTHER(x,y)) v PARENT(x,y)")
        #self.clause_list.append("!(PARENT(x,y)) v !(ALIVE(x)) v OLDER(x,y)")
        
        return self.clause_list

    def getclauses(self):
        return self.clause_list