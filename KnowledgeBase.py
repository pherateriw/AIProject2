import WorldGenerator as wg

# the explorer's knowledge base, what it knows about the environment
class KnowledgeBase:
    def __init__(self, size, oProbs, pProbs, wProbs):
        
        self.unknown_map = wg.createWorld(size, oProbs, pProbs, wProbs)
        self.known_map = wg.createGrid(size);
        self.percepts = {} 

        print("Actual map")        
        wg.printGrid(self.unknown_map)     
                
        print("Known map")
        wg.printGrid(self.known_map)

    def update_cell(self, x, y, char):
        self.known_map[x][y] = char
        if char != "_": # limit amount of maps printed
            wg.printGrid(self.known_map)

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
        if self.unknown_map[x][y] == 'g':            
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
            if (x - 1) >= 0:        
                if self.unknown_map[x - 1][y] == 'p':    
                    print("Explorer feels a breeze in ({},{})".format(x,y))
                    percept_breeze = 'b'
        
        # make sure is a valid choice for this y value   
        if y < len(self.known_map) - 1:        
            if self.unknown_map[x][y + 1] == 'p':    
                print("Explorer feels a breeze in ({},{})".format(x,y))
                percept_breeze = 'b'
                
            if y - 1 >= 0:          
                if self.unknown_map[x][y - 1] == 'p': 
                    print("Explorer feels a breeze in ({},{})".format(x,y))
                    percept_breeze = 'b'
        
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
        if (x - 1) >= 0:        
            if self.unknown_map[x - 1][y] == 'w':    
                print("Explorer smells a stench in ({},{})".format(x,y))
                percept_stench = 's'
        
        # make sure is a valid choice for this y value   
        if y < len(self.known_map) - 1:        
            if self.unknown_map[x][y + 1] == 'w':    
                print("Explorer smells a stench in ({},{})".format(x,y))
                percept_stench = 's'
                
            if y - 1 >= 0:          
                if self.unknown_map[x][y - 1] == 'w': 
                    print("Explorer smells a stench in ({},{})".format(x,y))
                    percept_stench = 's'
        
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
