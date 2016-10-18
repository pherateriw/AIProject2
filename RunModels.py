import Dudes
import argparse

def main():
    print("Hello Wumpus World!")
    parser = argparse.ArgumentParser()
    parser.add_argument("size", help="Size of world", type=int)
    parser.add_argument("obstacles", help="Probability of obstacles", type=float)
    parser.add_argument("pit", help="Probability of pits", type=float)
    parser.add_argument("wumpi", help="Probability of wumpi", type=float)
    args = parser.parse_args()

    dude = Dudes.ReactiveDude(args.size, args.obstacles, args.pit, args.wumpi)

if __name__ == '__main__':
    main()