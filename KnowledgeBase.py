import WorldGenerator as wg


class KnowledgeBase:
    def __init__(self, size, oProbs, pProbs, wProbs):
        self.unknown_map = wg.createWorld(size, oProbs, pProbs, wProbs)
        print(self.unknown_map)
