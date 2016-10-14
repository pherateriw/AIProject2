import KnowledgeBase
import Move
import random


class AbstractDude:

    def __init__(self, size, oProbs, pProbs, wProbs):
        self.kb = KnowledgeBase.KnowledgeBase(size, oProbs, pProbs, wProbs)
        self.size = size
        Move.place_dude(self.kb)
        self.x = 0
        self.y = 0

    # Not tested
    def get_neighbor_cells(self, x, y):
        neighbors = []
        # North
        if x > 0:
            neighbors.append((x-1, y))
        # East
        if x < self.size:
            neighbors.append((x+1, y))
        # South
            if y > 0:
                neighbors.append((x, y - 1))
        # West
            if y < self.size:
                neighbors.append((x, y + 1))
        return neighbors

    def get_possible_directions(self, x, y):
        directions = []
        if x > 0:
            directions.append("NORTH")
        if x < self.size:
            directions.append("EAST")
        if y < self.size:
            directions.append("SOUTH")
        if y > 0:
            directions.append("WEST")
        return directions


class ReactiveDude(AbstractDude):

    def __init__(self, size, oProbs, pProbs, wProbs):
        print("Reactive dude created!")
        super(ReactiveDude, self).__init__(size, oProbs, pProbs, wProbs)
        self.rounds()

    def rounds(self):
        while(True):
            self.get_random_safe()

    def get_random_safe(self):
        safe_directions = self.get_possible_directions(self.x, self.y)
        self.x, self.y = Move.move_direction(self.kb, self.x, self.y, random.choice(safe_directions))
