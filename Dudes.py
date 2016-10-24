import KnowledgeBase
import Move
import random
import InferenceEngine

class AbstractDude:

    def __init__(self, logger, kb, runnum):
        self.logger = logger
        self.kb = kb
        self.size = len(kb.known_map)
        self.move = Move.Move(self.logger, self.kb, self)
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
        self.runnum = runnum

    def print_stats_log(self):
        self.logger.warning("{},{},{},{},{},{},{}".format(self.runnum, self.move.moves, self.move.cost, (self.death_by_pit + self.death_by_wumpii), self.death_by_pit, self.killed_wumpii, self.cells_explored))


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

    def __init__(self, logger, kb, k):
        super(ReactiveDude, self).__init__(logger, kb, k)
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

    def __init__(self, logger, kb, k):
        super(InformedDude, self).__init__(logger, kb, k)
        self.logger.info("Informed dude created!")
        self.logger.info()
        self.ie = InferenceEngine.InferenceEngine(kb)
        self.move.place_dude()
        self.ie.tell(['a'], self.x, self.y)
        self.rounds()

    # while not gold found or stuck, keep moving.
    def rounds(self):
        t = 0  # time step TODO time?
        stop = False
        
        while not stop:
            # update percepts
            current_percepts = self.update_percepts(self.x, self.y)
            print(current_percepts)



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



