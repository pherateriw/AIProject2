# TODO add_use change_direction method/Move
# TODO add shoot arrow, wumpus scream
# TODO right now game does not end on pit/wumpus (helps to test), fix this
# TODO finish game/print stats if die
# TODO figure out why "None" is printing out and fix it
# TODO print statements in a more reasonable order?
# TODO check score
# TODO: arrows (in kb?)
# TODO: add other percept call
import WorldGenerator as wg


class Move:

    NORTH = '^'
    EAST = '>'
    SOUTH = 'v'
    WEST = '<'

    def __init__(self, kb, dude):
        self.gold_found = False
        self.kb = kb
        self.moves = 0
        self.cost = 0
        self.dude = dude

    # TODO if cases are getting copy/pasty modularize further?
    def move_direction(self, x, y, direction):
        self.moves += 1
        self.cost -= 1
        if direction == "^":
            print("Moving North")
            temp = x
            temp -= 1
            if self.successful_move(temp, y, direction):
                self.kb.update_cell(x, y, "_")
                x = temp
        if direction == "v":
            print("Moving South")
            temp = x
            temp += 1
            if self.successful_move(temp, y, direction):
                self.kb.update_cell(x, y, "_")
                x = temp
        if direction == ">":
            print("Moving East")
            temp = y
            temp += 1
            if self.successful_move(x, temp, direction):
                self.kb.update_cell(x, y, "_")
                y = temp
        if direction == "<":
            print("Moving West")
            temp = y
            temp -= 1
            if self.successful_move(x, temp, direction):
                self.kb.update_cell(x, y, "_")
                y = temp
        self.kb.update_cell(x, y, direction)
        return x, y, self.gold_found

    def place_dude(self):
        print("Placing Dude at (0, 0), facing south")
        self.kb.update_cell(0, 0, "v")
        self.kb.update_percept(0, 0)

    # upon move, interacts with the world (if in a relevant part of the map)
    def successful_move(self, x, y, direction):
        self.change_direction(direction)
        if self.kb.unknown_map[x][y] == 'g':
            self.grab_gold()
            return True
        elif self.kb.unknown_map[x][y] == 'o':
            self.kb.update_cell(x, y, "o")
            self.kb.update_percept(x, y)
            return False
        elif self.kb.unknown_map[x][y] == 'p':    
            self.pit_fall()
            self.kb.update_cell(x, y, "p")
            return True
        elif self.kb.unknown_map[x][y] == 'w':    
            self.wumpus_encounter()
            self.kb.update_cell(x, y, "w")
            return True
        return True

    def change_direction(self, direction):
        direction_dict = {'^': 0, '>': 1, 'v': 2, '<': 3}
        direction_list = ['^', '>', 'v', '<']
        current = self.kb.known_map[self.dude.x][self.dude.y]
        current = direction_dict.get(current)
        direction = direction_dict.get(direction)
        # No need to turn
        if direction == current:
            return
        elif direction - current == -1:
            print("Turning Left")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction])
            self.cost -= 1
        elif direction - current == 1:
            print("Turning Right")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction])
            self.cost -= 1
        elif direction - current == -2:
            print("Turning Left")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction + 1])
            self.cost -= 1
            print("Turning Left")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction])
            self.cost -= 1
        elif direction - current == 2:
            print("Turning Right")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction - 1])
            self.cost -= 1
            print("Turning Right")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction])
            self.cost -= 1
        elif direction - current == 3:
            print("Turning Left")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction])
            self.cost -= 1
        elif direction - current == -3:
            print("Turning Right")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction])
            self.cost -= 1
        else:
            print("Got turned around...")


    def grab_gold(self):
        print("Gold found!")
        self.moves += 1
        self.cost += 1000
        self.gold_found = True
        
    def pit_fall(self):
        print("Ahhhhhhhhhhhhhhhhhhhh!")
        print("RIP Explorer, you fell into a pit.")
        self.moves += 1
        self.cost -= 1000
        self.game_over = True     

    def wumpus_encounter(self):
        print("Crunch.")        
        print("RIP Explorer, you were eaten by a wumpus.")
        self.moves += 1
        self.cost -= 1000
        self.game_over = True  
        