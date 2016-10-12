import KnowledgeBase


class AbstractDude:

    def __init__(self, size, oProbs, pProbs, wProbs):
        self.kb = KnowledgeBase.KnowledgeBase(size, oProbs, pProbs, wProbs)


class ReactiveDude(AbstractDude):
    def __init__(self, size, oProbs, pProbs, wProbs):
        print("Reactive dude created!")
        super(ReactiveDude, self).__init__(size, oProbs, pProbs, wProbs)