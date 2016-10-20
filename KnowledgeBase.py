import WorldGenerator as wg

# the explorer's knowledge base, reflects what it knows about the environment
class KnowledgeBase:
    def __init__(self, size, oProbs, pProbs, wProbs):
        
        self.unknown_map = wg.createWorld(size, oProbs, pProbs, wProbs)
        self.known_map = wg.createGrid(size);
        self.percepts = {} 
        self.facts = {}
        self.clause_list = []
        self.ppits = []
        self.pwumpi = []
        
        print("Actual map")        
        wg.printGrid(self.unknown_map)     
                
        print("Known map")
        wg.printGrid(self.known_map)

    def update_cell(self, x, y, char):
        self.known_map[x][y] = char
        wg.printGrid(self.known_map)

    def update_unknown_cell(self, x, y, char):
        self.unknown_map[x][y] = char

    # update the percepts according to the environment    
    def update_percept(self, x, y):
        percept_key = "{%d,%d}" % (x, y)    
        self.percepts.setdefault(percept_key,[])
        
        pCount = 0;
        percept_glimmer = ''
        percept_breeze = ''
        percept_stench = '' 
        percept_thump = ''

        for value in self.percepts[percept_key]:
            pCount = len(value)
        
        # gold is in this cell, glimmer ($) is perceived, else (_) 
        if self.unknown_map[x][y] == '$':            
            print("Explorer sees a glimmer in ({},{})".format(x,y))
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
                print("Explorer feels a breeze in ({},{})".format(x,y))
                percept_breeze = 'b'
                self.set_potentials(x, y, 'd')
            if (x - 1) >= 0:        
                if self.unknown_map[x - 1][y] == 'p':    
                    print("Explorer feels a breeze in ({},{})".format(x,y))
                    percept_breeze = 'b'
                    self.set_potentials(x, y, 'd')
        
        # make sure is a valid choice for this y value   
        if y < len(self.known_map) - 1:        
            if self.unknown_map[x][y + 1] == 'p':    
                print("Explorer feels a breeze in ({},{})".format(x,y))
                percept_breeze = 'b'
                self.set_potentials(x, y, 'd')
                
            if y - 1 >= 0:          
                if self.unknown_map[x][y - 1] == 'p': 
                    print("Explorer feels a breeze in ({},{})".format(x,y))
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
                print("Explorer smells a stench in ({},{})".format(x,y))
                percept_stench = 's'
                self.set_potentials(x, y, 'm')
        if (x - 1) >= 0:        
            if self.unknown_map[x - 1][y] == 'w':    
                print("Explorer smells a stench in ({},{})".format(x,y))
                percept_stench = 's'
                self.set_potentials(x, y, 'm')
        
        # make sure is a valid choice for this y value   
        if y < len(self.known_map) - 1:        
            if self.unknown_map[x][y + 1] == 'w':    
                print("Explorer smells a stench in ({},{})".format(x,y))
                percept_stench = 's'
                self.set_potentials(x, y, 'm')
                
            if y - 1 >= 0:          
                if self.unknown_map[x][y - 1] == 'w': 
                    print("Explorer smells a stench in ({},{})".format(x,y))
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
            print("Explorer feels a thump in ({},{})".format(x,y))
            percept_thump = 't'
        else: 
            # no obstacle is perceived, update percept
            percept_thump = '_'

        # add the appropriate stench (wumpus) percept for this (x,y)
        if (pCount == 0):        
            self.percepts[percept_key].append(percept_thump)  

        print("########Explorer's Percepts:")
        for key, value in self.percepts.items():
            print(key, value)
        print("############################")
        print()        

        # take the information gathered from percepts, add it to the knowledge base
        for value in self.percepts[percept_key]:
            if (value != '_'):
                self.tell(percept_key, value, x, y) 


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





    # TODO: add safe spaces
    # TODO: add death info to cell, add inferred info to cell     
    # update the knowledge base with information gathered from percept
    def tell(self, key, assertion, x, y):        
        self.facts.setdefault(key,[])
        
        # for percept information, builds the appropriate assertion
        if (assertion == '$'):
            assertion = "GLIMMER({},{})".format(x,y)
        elif (assertion == 'b'):
            assertion = "BREEZE({},{})".format(x,y)
        elif (assertion == 's'):
            assertion = "STENCH({},{})".format(x,y)
        elif (assertion == 't'):
            assertion = "BUMP({},{})".format(x,y)
       
       # check that this rule is not already in dictionary
        if (assertion not in self.facts[key]):
            self.facts[key].append(assertion)       
        
        print("########Information in Knowledge Base:")
        for key, value in self.facts.items():
            print(key, value)
        print("##################################")
        print()        

    # TODO: write this
    # ask questions of the knowledge base
    # input: kb, query
    def ask():
        print("not implemented yet")

    # TODO: quantifiers?
    def clauses(self):
        """Creates and returns a list of clauses in the knowledge base.
        All Predicates with all caps, Instantiated variables with single capital letter at beginning,
        Uninstantiated variables lowercase char (cannot include v since v means or)
        All sentences in clause form
        Possble Actions: GRAB, TURN90, MOVEFORWARD, SHOOTARROW
        Possible Predicates: SAFE(X,Y), BREEZE(X,Y), STENCH(X,Y), BUMP(X,Y), PIT(X,Y), WUMPUS(X,Y), OBSTACLE(X,Y),
        GOLD(X,Y), POSSPIT(X,Y), POSSWUMP(X,Y), AT(X,Y)(?)
        """
        self.clause_list.append("BUMP(X,Y) => OBSTACLE(X,Y)") #If there's a bump, there must be an obstacle
        self.clause_list.append("SAFE(X,Y) <=> !(PIT(X,Y)) ^ !(WUMPUS(X,Y)") #If it's safe there are no pits or wumpi
        self.clause_list.append("BREEZE(X,Y) <=> (PIT(X+1,Y) v PIT(X-1,Y) v PIT(X,Y+1) v PIT(X,Y-1))") #A breeze means there must be a pit in one of the surrounding cells
        self.clause_list.append("STENCH(X,Y) <=> (WUMPUS(X+1,Y) v WUMPUS(X-1,Y) v WUMPUS(X,Y+1) v WUMPUS(X,Y-1))") #A stench means there must be a wumpus in one of the surrounding cells
        self.clause_list.append("POSSPIT(X,Y) ^ SAFE(X,Y) => !PIT(X,Y)") #A Possible Pit that is already safe means there is no pit there
        self.clause_list.append("POSSWUMP(X,Y) ^ SAFE(X,Y) => !WUMPUS(X,Y)")#A Possible Wumpus that is already safe means there is no wumpus there
        self.clause_list.append("PIT(X,Y) => !SAFE(X,Y) ^ !WUMPUS(X,Y)") #Pits, wumpi and safe can not be in the same cells
        self.clause_list.append("WUMPUS(X,Y) => !SAFE(X,Y) ^ !PIT(X,Y)")
        self.clause_list.append("BREEZE(X,Y) => (POSSPIT(X+1,Y) ^ POSSPIT(X-1,Y) ^ POSSPIT(X,Y+1) ^ POSSPIT(X,Y-1))") 
        self.clause_list.append("STENCH(X,Y) => (POSSWUMP(X+1,Y) ^ POSSWUMP(X-1,Y) ^ POSSWUMP(X,Y+1) ^ POSSWUMP(X,Y-1))")


        
        # Jani: change this if needed, was just testing to make sure I could reach this 

        for c in self.clause_list:
            if "magic regex" in c: #TODO: find implications and remove them from clause list
                print(c)

                
        for c in self.clause_list: 
            print (c)
        
        return self.clause_list

    def getclauses(self):
        return self.clause_list