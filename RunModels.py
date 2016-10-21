import Dudes
import argparse
import KnowledgeBase

class RunModels:

    def save_file(self, fn, arrows, kb):
        outf = open(fn, 'w')
        outf.write(str(arrows))
        outf.write('\n')
        for line in kb.unknown_map:
            for l in line:
                outf.write(l)
            outf.write('\n')
        outf.close()


    def load_file(self, fn):
        infile = open(fn, 'r')
        line = infile.readline()
        num_arrows = int(line.strip('\n'))
        result = [list(line.strip('\n')) for line in infile]
        infile.close()
        return result, num_arrows

    def create_sizes(self, obstacles, wumpi, pits):
        for i in range(5, 30, 5):
            for k in range(5):
                kb = KnowledgeBase.KnowledgeBase(i, obstacles, wumpi, pits, None)
                fn = "test_worlds/sizes/size%s/test%s" % (i, k)
                self.save_file(fn, kb.numWumpii, kb)

    def create_probs(self, obstacles, wumpi, pits):
        probs5 = [.12, .23/3, .46/3, .69/3, .92/3]
        self.create_single_prob(5, probs5)
        probs10 = [.03, .245/3, .49/3, .735/3, .98/3]
        self.create_single_prob(10, probs10)
        probs15 = [.012, .248/3, .496/3, .743/3, .991/3]
        self.create_single_prob(15, probs15)
        probs20 = [.009, .249/3, .498/3, .746/3, .995/3]
        self.create_single_prob(20, probs20)
        probs25 = [.006, .25/3, .5/3, .75/3, .997/3]
        self.create_single_prob(25, probs25)

    def create_single_prob(self, size, prob):
        for p in prob:
            for i in range(5):
                kb = KnowledgeBase.KnowledgeBase(size, p, p, p, None)
                fn = "test_worlds/probs/size{}/probs{:.3f}/test{}".format(size, p, i)
                self.save_file(fn, kb.numWumpii, kb)

def main():
    print("Hello Wumpus World!")
    parser = argparse.ArgumentParser()
    parser.add_argument("size", help="Size of world", type=int)
    parser.add_argument("obstacles", help="Probability of obstacles", type=float)
    parser.add_argument("pits", help="Probability of pits", type=float)
    parser.add_argument("wumpi", help="Probability of wumpi", type=float)
    args = parser.parse_args()
    rm = RunModels()

    load_file = False
    save_file = True

    # rm.create_sizes(args.obstacles, args.wumpi, args.pits)
    rm.create_probs(args.obstacles, args.wumpi, args.pits)

    # if load_file:
    #     kb = KnowledgeBase.KnowledgeBase(args.size, args.obstacles, args.wumpi, args.pits, rm.load_file("test1"))
    # else:
    #     kb = KnowledgeBase.KnowledgeBase(args.size, args.obstacles, args.wumpi, args.pits,  None)
    # arrows = kb.numWumpii
    # if save_file:
    #     rm.save_file("test_worlds/size5/test2", arrows, kb)


    # TODO: make a choice for user, make sure we pass same world to both
    # rDude = Dudes.ReactiveDude(kb)
    # iDude = Dudes.InformedDude(kb)



if __name__ == '__main__':
    main()