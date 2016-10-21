import KnowledgeBase
import Move
import random
import InferenceEngine

class AbstractDude:

    def __init__(self, kb):
        self.kb = kb
        self.size = len(kb.known_map)
        self.move = Move.Move(self.kb, self)
        self.x = 0
        self.y = 0
        self.prevx = 0
        self.prvey = 0
        self.death_by_pit = 0
        self.death_by_wumpii = 0
        self.killed_wumpii = 0
        self.arrows = self.kb.numWumpii
        self.cells_explored = 0

    def print_stats(self):
        print("Total Moves: %s" % self.move.moves)
        print("Total Cost: %s" % self.move.cost)
        print("Total Death: %s" % (self.death_by_pit + self.death_by_wumpii))
        print("Wumpii Deaths: %s" % self.death_by_wumpii)
        print("Pit Deaths: %s" % self.death_by_pit)
        print("Wumpii Killed: %s" % self.killed_wumpii)
        print("Cells explored: %s" % self.cells_explored)

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

    def __init__(self, kb):
        print("Reactive dude created!")
        super(ReactiveDude, self).__init__(kb)
        self.move.place_dude()
        self.rounds()

    def rounds(self):
        go_on = False
        while not go_on :
            go_on = self.get_random_safe()
        self.print_stats()

    def get_random_safe(self):
        safe, unsafe = self.get_possible_directions(self.x, self.y)
        if len(safe) > 0:
            choices = safe
        elif len(unsafe) >0:
            choices = unsafe
        else:
            print("Explorer is stuck!!")
            return True
        self.x, self.y, gold_found = self.move.move_direction(self.x, self.y, random.choice(choices))
        return gold_found

# TODO: comment this, change so works as expected
# TODO: how to turn right/left? double check with Lisa
class InformedDude(AbstractDude):

    def __init__(self, kb):
        print("Informed dude created!")
        print()
        super(InformedDude, self).__init__(kb)
        self.ie = InferenceEngine.InferenceEngine(kb)
        self.move.place_dude()
        self.ie.tell('{0,0}', 'a', self.x, self.y) # 0, 0 is safe
        self.rounds()

    def rounds(self):
        t = 0 # time sequence
        go_on = True
        while go_on:
            choice = self.ie.ask()
            percept, go_one = self.make_move(choice)
            self.ie.tell(percept)

    def makePerceptSentence(self, x, y):
        #Percept structure: [GLITTER, BUMP, STENCH, BREEZE, TIMESTEP]
        percept  = [True, False, True, False, 3]
        return percept


    # TODO: make sure matches design doc
    # R & N pg 270, adapted to FOL
    # inputs: percepts
    # persistent: kb, plan (action sequence, starts empty)
    # TELL(KB, MAKE-PERCEPT-SENTENCE(percept,t))
    # TELL the KB the temporal physics sentences for time t    

    def make_move(self, choice):
        percept = ""
        go_on = True
        return percept, go_on



