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

        #stats
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
    """
    Reactive Dude does not do any reasoning about world, he simply choose randomly from among his possible choices.
    """

    def __init__(self, kb):
        print("Reactive dude created!")
        super(ReactiveDude, self).__init__(kb)
        self.move.place_dude()
        self.rounds()

    # while not gold found or stuck, keep moving.
    def rounds(self):
        stop = False
        while not stop:
            stop = self.make_move()
        self.print_stats()

    # Get directions to move in, move, return result
    def make_move(self):
        safe, unsafe = self.get_possible_directions(self.x, self.y)
        # No safe or unsafe choices
        if len(safe) > 0:
            choices = safe
        elif len(unsafe) >0:
            choices = unsafe
        else:
            print("Explorer is stuck!!")
            return True
        # new x, new y and bool for found gold
        self.x, self.y, gold_found = self.move.move_direction(self.x, self.y, random.choice(choices))
        return gold_found


class InformedDude(AbstractDude):
    """
    Informed dude will explore the world, updated the Knowledge Base as he does so and querying the Inference Engine
    for next move.
    """

    def __init__(self, kb):
        print("Informed dude created!")
        print()
        super(InformedDude, self).__init__(kb)
        self.ie = InferenceEngine.InferenceEngine(kb)
        self.move.place_dude()
        self.ie.tell(['a'], self.x, self.y)
        self.rounds()

    # while not gold found or stuck, keep moving.
    def rounds(self):
        t = 0 # time step TODO time?
        stop = False
        while not stop:
            choices = self.ie.ask("What Next?", self.x, self.y)  # Ask Inference Engine for best possible choices
            if 'stuck' in choices:
                stop = True
                break
            stop, percept = self.make_move(random.choice(choices))
            if percept:  # new percept
                self.ie.tell(percept, self.x, self.y)

    # Make move, return new x, new y, and if gold found
    def make_move(self, choice):
        self.x, self.y, stop, percept = self.move.move_direction(self.x, self.y, choice)
        return stop, percept



