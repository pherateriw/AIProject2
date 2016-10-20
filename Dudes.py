import KnowledgeBase
import Move
import random
import InferenceEngine

class AbstractDude:

    def __init__(self, size, oProbs, pProbs, wProbs):
        self.kb = KnowledgeBase.KnowledgeBase(size, oProbs, pProbs, wProbs)
        self.size = size
        self.move = Move.Move(self.kb, self)
        self.move.place_dude()
        self.x = 0
        self.y = 0
        self.prevx = 0
        self.prvey = 0
        self.arrow = self.kb.numWumpii
        self.death_by_pit = 0
        self.death_by_wumpii = 0
        self.wumpii_kill = 0
        self.total_deaths = self.death_by_pit + self.death_by_wumpii


    def get_possible_directions(self, x, y):
        safe_directions = []
        unsafe_directions = []
        unsafe_chars = ['d', 'm']
        impossible_chars = ['o', 'p', 'w', 's']
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

        # Retracing steps and killing wumpii is last resort
        if len(safe_directions) == 0 and len(unsafe_directions) == 0:
            if x > 0:
                if self.kb.known_map[x - 1][y] == 'w':
                    safe_directions.append("^k")
                elif self.kb.known_map[x - 1][y] == 's':
                    safe_directions.append('^')
            if x < self.size -1:
                if self.kb.known_map[x + 1][y] == 'w':
                    safe_directions.append("vk")
                elif self.kb.known_map[x + 1][y] == 's':
                    safe_directions.append('v')
            if y > 0:
                if self.kb.known_map[x][y - 1] == 'w':
                    safe_directions.append("<k")
                elif self.kb.known_map[x][y - 1] == 's':
                    safe_directions.append('<')
            if y < self.size -1:
                if self.kb.known_map[x][y + 1] == 'w':
                    safe_directions.append(">k")
                elif self.kb.known_map[x][y + 1] == 's':
                    safe_directions.append('>')
        return safe_directions, unsafe_directions


class ReactiveDude(AbstractDude):

    def __init__(self, size, oProbs, pProbs, wProbs):
        print("Reactive dude created!")
        super(ReactiveDude, self).__init__(size, oProbs, pProbs, wProbs)
        self.rounds()

    def rounds(self):
        go_on = False
        while not go_on :
            go_on = self.get_random_safe()
        print("Total Moves")
        print(self.move.moves)
        print("Total Cost")
        print(self.move.cost)

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

    def __init__(self, size, oProbs, pProbs, wProbs):
        print("Informed dude created!")
        print()
        super(InformedDude, self).__init__(size, oProbs, pProbs, wProbs)
        self.rounds()

    def rounds(self):
        self.move.informed_dude_move()

        #go_on = False
        #while not go_on :
        #    go_on = self.get_random_safe()
        #print("Total Moves")
        #print(self.move.moves)
        #print("Total Cost")
        #print(self.move.cost)

    def get_random_safe(self):
        safe_directions = self.get_possible_directions(self.x, self.y)
        self.x, self.y, gold_found = self.move.move_direction(self.x, self.y, random.choice(safe_directions))
        return gold_found
        
    # TODO: make sure matches design doc    
    # R & N pg 270, adapted to FOL
    # inputs: percepts
    # persistent: kb, plan (action sequence, starts empty)
    # TELL(KB, MAKE-PERCEPT-SENTENCE(percept,t))
    # TELL the KB the temporal physics sentences for time t    




