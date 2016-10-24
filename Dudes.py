import KnowledgeBase
import Move
import random
import InferenceEngine

class AbstractDude:

    def __init__(self, logger, kb, runnum, prob):
        self.logger = logger
        self.kb = kb
        self.size = len(kb.known_map)
        self.move = Move.Move(self.logger, self.kb, self)
        self.x = 0
        self.y = 0
        self.prevx = 0
        self.prvey = 0
        self.prob = prob

        #stats
        self.death_by_pit = 0
        self.death_by_wumpii = 0
        self.killed_wumpii = 0
        self.arrows = self.kb.numWumpii
        self.cells_explored = 0
        self.runnum = runnum


    def print_stats_log(self):
        total_death = self.death_by_pit + self.death_by_wumpii
        self.logger.warning("{},{:.3f},{},{},{},{},{},{},{},{}".format(
            self.size, self.prob, self.runnum, self.move.moves,
            self.move.cost, total_death, self.death_by_pit,
            self.death_by_wumpii, self.killed_wumpii, self.cells_explored))

    def print_stats_console(self):
        print("##########")
        print("##########")
        print("Final Stats")
        print("Total Moves: %s" % self.move.moves)
        print("Total Cost: %s" % self.move.cost)
        print("Total Death: %s" % (self.death_by_pit + self.death_by_wumpii))
        print("Wumpii Deaths: %s" % self.death_by_wumpii)
        print("Pit Deaths: %s" % self.death_by_pit)
        print("Wumpii Killed: %s" % self.killed_wumpii)
        print("Cells explored: %s" % self.cells_explored)
        print("##########")
        print("##########")
        print("")
        print("")

    # get potential directions to go in preference order of:
    # unexplored and safe seeming cells
    # unexplored but unsafe seeming cells
    # killing a wumpus
    # safe cells
    def get_possible_directions(self, x, y):
        safe_directions = []
        unsafe_directions = []
        unsafe_chars = ['d', 'm']  # Potential wumpi or pits
        impossible_chars = ['o', 'p', 'w', 's'] # For sure obstacles, pits, wumpii, and already traveled and safe cells
        if x > 0:
            if self.kb.known_map[x - 1][y] not in unsafe_chars and self.kb.known_map[x - 1][y] not in impossible_chars:
                safe_directions.append("^")
            elif self.kb.known_map[x - 1][y] not in impossible_chars:
                unsafe_directions.append("^")
        if x < self.size - 1:
            if self.kb.known_map[x + 1][y] not in unsafe_chars and self.kb.known_map[x + 1][y] not in impossible_chars:
                safe_directions.append("v")
            elif self.kb.known_map[x + 1][y] not in impossible_chars:
                unsafe_directions.append('v')
        if y < self.size -1 :
            if self.kb.known_map[x][y + 1] not in unsafe_chars and self.kb.known_map[x][y + 1] not in impossible_chars:
                safe_directions.append(">")
            elif self.kb.known_map[x][y + 1] not in impossible_chars:
                unsafe_directions.append(">")
        if y > 0:
            if self.kb.known_map[x][y - 1] not in unsafe_chars and self.kb.known_map[x][y -1] not in impossible_chars:
                safe_directions.append("<")
            elif self.kb.known_map[x][y - 1] not in impossible_chars:
                unsafe_directions.append("<")

        # No choice kill a wumpii, or retrace steps
        if len(safe_directions) == 0 and len(unsafe_directions) == 0:
            if x > 0:
                if self.kb.known_map[x - 1][y] == 'w' and self.arrows > 0:
                    safe_directions.append("^k")
                elif self.kb.known_map[x - 1][y] == 's':
                    unsafe_directions.append('^')
            if x < self.size - 1:
                if self.kb.known_map[x + 1][y] == 'w' and self.arrows > 0:
                    safe_directions.append("vk")
                elif self.kb.known_map[x + 1][y] == 's':
                    unsafe_directions.append('v')
            if y > 0:
                if self.kb.known_map[x][y - 1] == 'w' and self.arrows > 0:
                    safe_directions.append("<k")
                elif self.kb.known_map[x][y - 1] == 's':
                    unsafe_directions.append('<')
            if y < self.size -1:
                if self.kb.known_map[x][y + 1] == 'w' and self.arrows > 0:
                    safe_directions.append(">k")
                elif self.kb.known_map[x][y + 1] == 's':
                    unsafe_directions.append('>')

        return safe_directions, unsafe_directions


class ReactiveDude(AbstractDude):
    """
    Reactive Dude does not do any reasoning about world, he simply choose randomly from among his possible choices.
    """

    def __init__(self, logger, kb, k, prob):
        super(ReactiveDude, self).__init__(logger, kb, k, prob)
        self.logger.info("Reactive dude created!")
        self.move.place_dude()
        self.rounds()

    # while not gold found or stuck, keep moving.
    def rounds(self):
        stop = False
        while not stop:
            stop = self.make_move()
        self.print_stats_log()

    # Get directions to move in, move, return result
    def make_move(self):
        safe, unsafe = self.get_possible_directions(self.x, self.y)
        # No safe or unsafe choices
        if len(safe) > 0:
            choices = safe
        elif len(unsafe) >0:
            choices = unsafe
        else:
            self.logger.info("Explorer is stuck!!")
            return True
        # new x, new y and bool for found gold
        self.x, self.y, gold_found, percept = self.move.move_direction(self.x, self.y, random.choice(choices))
        return gold_found


class InformedDude(AbstractDude):
    """
    Informed dude will explore the world, updated the Knowledge Base as he does so and querying the Inference Engine
    for next move.
    """

    def __init__(self, logger, kb, k, prob):
        super(InformedDude, self).__init__(logger, kb, k, prob)
        self.logger.info("Informed dude created!")
        self.ie = InferenceEngine.InferenceEngine(kb)
        self.move.place_dude()
        self.ie.tell(['a'], self.x, self.y)
        self.rounds()

    # while not gold found or stuck, keep moving.
    def rounds(self):
        #t = 0  # time step TODO time?
        stop = False
        choices = []
        current_valid_choices = set()
               
        
        while not stop:
            # update the explorer's percepts for the current location
            current_percept_key = self.kb.update_percept(self.x, self.y)
            
            # tell the knowledge base information gathered from these percepts
            if current_percept_key != None:            
                for value in current_percept_key:
                    if value != '_':
                        self.ie.tell(value, self.x, self.y)

            # try to infer a plan of action for the next move                
            # gets move based on answers to the following queries (prioritized via order of questions)
            # build our choice of move based on inference
            # note, in the absence of a glimmer, the highest priority moves are those unvisited cells that we believe to be safe, followed by potentially riskier moves (cells not known to be safe)

            choices_Gold = ""
            choices_Safe = ""
            choices_perNoStench = ""
            choices_perNoBreeze = ""
            choices_perNoObstacle = ""
            choices_notWumpus = ""
            choices_notPit = ""
            choices_notObstacle = ""            
            choices_Wumpus = ""
            choices_Pit = ""
            choices_Obstacle = ""
            
            if self.x >= 0 and self.x <= self.size:
                # explorer can only grab gold when in the same square as the glimmer, and grabbing the gold is the highest priority move
                choices_Gold = self.ie.ask("GLIMMER({},{})".format(self.x, self.y), self.x, self.y)            
    
                # checks what directions are safe, adds them 
                choices_Safe = self.ie.ask("SAFE({},{})".format(self.x, self.y), self.x, self.y)
            
                # if we don't have SAFE(x,y) in KB, try to determine if cell is safe using percept info
                choices_perNoStench = self.ie.ask("!(STENCH({},{}))".format(self.x, self.y), self.x, self.y)
            
                choices_perNoBreeze = self.ie.ask("!(BREEZE({},{}))".format(self.x, self.y), self.x, self.y)                    
            
                choices_perNoObstacle = self.ie.ask("!(OBSTACLE({},{}))".format(self.x, self.y), self.x, self.y)   
            
                # if we don't know (and can't ascertain) if cell is safe, make checks that would allow a riskier move 
                choices_notWumpus = self.ie.ask("!(WUMPUS({},{}))".format(self.x, self.y), self.x, self.y) 
            
                choices_notPit = self.ie.ask("!(PIT({},{}))".format(self.x, self.y), self.x, self.y) 
            
                choices_notObstacle = self.ie.ask("!(OBSTACLE({},{}))".format(self.x, self.y), self.x, self.y)
              
                # look at hazards on map
                choices_Wumpus = self.ie.ask("WUMPUS({},{})".format(self.x, self.y), self.x, self.y) 
                        
                choices_Pit = self.ie.ask("PIT({},{})".format(self.x, self.y), self.x, self.y) 
                       
                choices_Obstacle = self.ie.ask("OBSTACLE({},{})".format(self.x, self.y), self.x, self.y)              
                                
                # add all possible choices together (with no duplicates) to determine the best choice
                if choices_Gold != "":
                    for c in choices_Gold:
                        choices.append(c)
                if choices_Safe != "":
                    for c in choices_Safe:
                        choices.append(c)
                if choices_perNoStench != "":
                    for c in choices_perNoStench:
                        choices.append(c)
                if choices_perNoBreeze != "":
                    for c in choices_perNoBreeze:
                        choices.append(c)
                if choices_perNoObstacle != "":
                    for c in choices_perNoObstacle:
                        choices.append(c)
                if choices_notWumpus != "":
                    for c in choices_notWumpus:
                        choices.append(c)
                if choices_notPit != "":
                    for c in choices_notPit:
                        choices.append(c)
                if choices_notObstacle != "":
                    for c in choices_notObstacle:
                        choices.append(c)
                if choices_Wumpus != "":
                    for c in choices_Wumpus:
                        choices.append(c)
                if choices_notPit != "":
                    for c in choices_Pit:
                        choices.append(c)
                if choices_notObstacle != "":
                    for c in choices_Obstacle:
                        choices.append(c)                
             
                for c in choices:
                    current_valid_choices.add(c)  
                    
                choices.clear()
    
                if 'Stuck' in current_valid_choices:
                    stop = True
                    self.logger.info("Explorer is stuck!")
                    break            
                
                if len(current_valid_choices) > 0:            
                    #print(list(current_valid_choices)[0])
                    if list(current_valid_choices)[0] == '<k' or list(current_valid_choices)[0] == '>k' or list(current_valid_choices)[0] == '^k' or list(current_valid_choices)[0] == 'vk':
                        self.kb.tell("SHOOTARROW({},{})".format(self.x, self.y), self.x, self.y)      
                        
                        if list(current_valid_choices)[0] == '<k':
                            stop, percept = self.make_move(random.choice('<'))
                            self.move.shoot_wumpus('<')
                        elif list(current_valid_choices)[0] == '>k':
                            stop, percept = self.make_move(random.choice('>'))
                            self.move.shoot_wumpus('>')                            
                        elif list(current_valid_choices)[0] == 'vk':
                            stop, percept = self.make_move(random.choice('v'))
                            self.move.shoot_wumpus('v')
                        elif list(current_valid_choices)[0] == '^k':
                            stop, percept = self.make_move(random.choice('^'))
                            self.move.shoot_wumpus('^')
                        else:
                            stop, percept = self.make_move(random.choice(list(current_valid_choices)[0]))                            
                            current_valid_choices.clear()
                  
                # roll the dice, if we are not stuck but it looks like we have no good moves
                stop, percept = self.make_move(random.choice(list(current_valid_choices)))   
                current_valid_choices.clear()

            choices = self.ie.ask("What Next?", self.x, self.y)  # Ask Inference Engine for best possible choices
            if 'Stuck' in choices:
                stop = True
                self.logger.info("Explorer is stuck!")
                break
            stop, percept = self.make_move(random.choice(choices))
            if percept:  # new percept
                self.ie.tell(percept, self.x, self.y)
        self.print_stats_log()


    # Make move, return new x, new y, and if gold found
    def make_move(self, choice):
        self.x, self.y, stop, percept = self.move.move_direction(self.x, self.y, choice)
        return stop, percept




