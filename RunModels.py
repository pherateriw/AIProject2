import Dudes
import argparse

def main():
    print("Hello Wumpus World!")
    parser = argparse.ArgumentParser()
    parser.add_argument("size", help="Size of world", type=int)
    parser.add_argument("o", help="Probability of obstacles", type=float)
    parser.add_argument("p", help="Probability of pits", type=float)
    parser.add_argument("w", help="Probability of wumpi", type=float)
    args = parser.parse_args()

    #rDude = Dudes.ReactiveDude(args.size, args.o, args.p, args.w)
    iDude = Dudes.InformedDude(args.size, args.o, args.p, args.w)
    
if __name__ == '__main__':
    main()