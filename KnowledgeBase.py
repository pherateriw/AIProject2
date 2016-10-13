import WorldGenerator as wg


class KnowledgeBase:
    def __init__(self, size, oProbs, pProbs, wProbs):
        self.unknown_map = wg.createWorld(size, oProbs, pProbs, wProbs)
        self.known_map = wg.createGrid(size);
        print("Actual map")
        print(self.unknown_map)
        print("Known map")
        print(self.known_map)

    def update_cell(self, x, y, char):
        self.known_map[x][y]= char
        print(self.known_map)
