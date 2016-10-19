import Dudes
import argparse

def main():
    print("Hello Wumpus World!")
    parser = argparse.ArgumentParser()
    parser.add_argument("size", help="Size of world", type=int)
    parser.add_argument("obstacles", help="Probability of obstacles", type=float)
    parser.add_argument("pits", help="Probability of pits", type=float)
    parser.add_argument("wumpi", help="Probability of wumpi", type=float)
    args = parser.parse_args()


    # TODO: make a choice for user, make sure we pass same world to both
    rDude = Dudes.ReactiveDude(args.size, args.obstacles, args.pits, args.wumpi)
    # iDude = Dudes.InformedDude(args.size, args.obstacles, args.pit, args.wumpi)
    
if __name__ == '__main__':
    main()