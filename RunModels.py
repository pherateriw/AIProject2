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
    if load_file:
        kb = KnowledgeBase.KnowledgeBase(args.size, args.obstacles, args.wumpi, args.pits, rm.load_file("test1"))
    else:
        kb = KnowledgeBase.KnowledgeBase(args.size, args.obstacles, args.wumpi, args.pits,  None)
    arrows = kb.numWumpii
    if save_file:
        rm.save_file("test_worlds/size5/test2", arrows, kb)

    # TODO: make a choice for user, make sure we pass same world to both
    # rDude = Dudes.ReactiveDude(kb)
    iDude = Dudes.InformedDude(kb)


if __name__ == '__main__':
    main()