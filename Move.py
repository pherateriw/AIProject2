# TODO: add other percept call

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

    def informed_dude_move(self, kb):
        from InferenceEngine import InferenceEngine
        ie = InferenceEngine(self.kb)
        
    def move_direction(self, x, y, direction):
        self.dude.cells_explored += 1
        self.dude.prevx = x
        self.dude.prevy = y
        self.moves += 1
        self.cost -= 1
        if len(direction) > 1:
            self.shoot_wumpus(direction)
            return x, y, self.gold_found
        if direction == "^":
            print("Moving North")
            temp = x
            temp -= 1
            if self.successful_move(temp, y, direction):
                x = temp
        if direction == "v":
            print("Moving South")
            temp = x
            temp += 1
            if self.successful_move(temp, y, direction):
                x = temp
        if direction == ">":
            print("Moving East")
            temp = y
            temp += 1
            if self.successful_move(x, temp, direction):
                y = temp
        if direction == "<":
            print("Moving West")
            temp = y
            temp -= 1
            if self.successful_move(x, temp, direction):
                y = temp
        self.kb.update_cell(x, y, direction)
        self.kb.update_percept(x, y)
        return x, y, self.gold_found

    def shoot_wumpus(self, direction):
        print("Killing a wumpus!!!")
        self.cost -= 10
        if direction[0] == '^':
            print("Shooting arrow north")
            i = self.dude.x
            y = self.dude.y
            while i >= 0:
                if self.kb.unknown_map[i][y] == 'w':
                    self.kill_wumpi(i, y)
                    break
                i -= 1
        elif direction[0] == '>':
            print("Shooting arrow west")
            x = self.dude.x
            i = self.dude.y
            while i < len(self.kb.known_map):
                if self.kb.unknown_map[x][i] == 'w':
                    self.kill_wumpi(x, i)
                    break
                i += 1
        elif direction[0] == 'v':
            print("Shooting arrow south")
            i = self.dude.x
            y = self.dude.y
            while i < len(self.kb.known_map):
                if self.kb.unknown_map[i][y] == 'w':
                    self.kill_wumpi(i, y)
                    break
                i += 1
        elif direction[0] == '<':
            print("Shooting arrow east")
            x = self.dude.x
            i = self.dude.y
            while i >= 0:
                if self.kb.unknown_map[x][i] == 'w':
                    self.kill_wumpi(x, i)
                    break
                i -= 1


    def kill_wumpi(self, x, y):
        print("AAAIIIIEEEEE")
        self.kb.update_cell(x, y, '_')
        self.kb.update_unknown_cell(x, y, '_')
        self.dude.arrows -= 1
        self.cost += 10
        self.dude.killed_wumpii += 1


    # places the explorer in the starting cell, facing south
    def place_dude(self):
        print("Placing Dude at (0, 0), facing south")
        self.kb.update_cell(0, 0, "v")
        self.kb.update_percept(0, 0)

    # upon move, interacts with the world (if in a relevant part of the map)
    def successful_move(self, x, y, direction):
        self.change_direction(direction)
        # if in square with gold, grab gold
        if self.kb.unknown_map[x][y] == '$':
            self.grab_gold()
            return True
        # don't update percept for square with obstacle
        elif self.kb.unknown_map[x][y] == 'o':
            self.kb.update_cell(x, y, "o")
            return False
        # if in square with pit, call pit fall handler
        elif self.kb.unknown_map[x][y] == 'p':    
            self.pit_fall()
            self.kb.update_cell(x, y, "p")
            return False
        # if in square with wumpus, call wumpus handler
        elif self.kb.unknown_map[x][y] == 'w':    
            self.wumpus_encounter()
            self.kb.update_cell(x, y, "w")
            return False
        else:
            self.kb.update_cell(self.dude.prevx, self.dude.prevy, 's')
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
        self.dude.death_by_pit += 1
        self.game_over = True     

    def wumpus_encounter(self):
        print("Crunch.")        
        print("RIP Explorer, you were eaten by a wumpus.")
        self.moves += 1
        self.cost -= 1000
        self.dude.death_by_wumpii += 1
        self.game_over = True  

