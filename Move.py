class Move:

    NORTH = '^'
    EAST = '>'
    SOUTH = 'v'
    WEST = '<'

    def __init__(self, logger, kb, dude):
        self.logger = logger
        self.gold_found = False
        self.kb = kb # Knowledge Base
        self.moves = 0
        self.cost = 0
        self.dude = dude
        self.cur_percept = None

    # Given direction, attempt to move in that direction or to shoot a wumpii.
    # Update Maps/knowledgeBase according to percepts
    # Keep track of stats for each type of move
    def move_direction(self, x, y, direction):
        self.dude.prevx = x
        self.dude.prevy = y
        self.moves += 1
        self.cost -= 1
        # Direction contains shoot char and direction to shoot
        if len(direction) > 1:
            self.shoot_wumpus(direction)
            return x, y, self.gold_found, self.cur_percept
        # Else moving a direction
        elif direction == "^":
            self.logger.info("Moving North")
            temp = x
            temp -= 1
            if self.successful_move(temp, y, direction):
                x = temp
        elif direction == "v":
            self.logger.info("Moving South")
            temp = x
            temp += 1
            if self.successful_move(temp, y, direction):
                x = temp
        elif direction == ">":
            self.logger.info("Moving East")
            temp = y
            temp += 1
            if self.successful_move(x, temp, direction):
                y = temp
        elif direction == "<":
            self.logger.info("Moving West")
            temp = y
            temp -= 1
            if self.successful_move(x, temp, direction):
                y = temp

        self.kb.update_cell(x, y, direction)
        self.cur_percept = self.kb.update_percept(x, y)
        return x, y, self.gold_found, self.cur_percept

    # Shooting an arrow in direction specified and listening for scream
    def shoot_wumpus(self, direction):
        self.logger.info("Killing a wumpus!!!")
        self.cost -= 10
        if direction[0] == '^':
            self.logger.info("Shooting arrow north")
            i = self.dude.x
            y = self.dude.y
            while i >= 0:
                if self.kb.unknown_map[i][y] == 'w':
                    self.wumpus_death(i, y)
                    break
                i -= 1
        elif direction[0] == '>':
            self.logger.info("Shooting arrow west")
            x = self.dude.x
            i = self.dude.y
            while i < len(self.kb.known_map):
                if self.kb.unknown_map[x][i] == 'w':
                    self.wumpus_death(x, i)
                    break
                i += 1
        elif direction[0] == 'v':
            self.logger.info("Shooting arrow south")
            i = self.dude.x
            y = self.dude.y
            while i < len(self.kb.known_map):
                if self.kb.unknown_map[i][y] == 'w':
                    self.wumpus_death(i, y)
                    break
                i += 1
        elif direction[0] == '<':
            self.logger.info("Shooting arrow east")
            x = self.dude.x
            i = self.dude.y
            while i >= 0:
                if self.kb.unknown_map[x][i] == 'w':
                    self.wumpus_death(x, i)
                    break
                i -= 1


    # Sucessfully killed a wumpus, sound scream and update stats
    def wumpus_death(self, x, y):
        self.logger.info("AAAIIIIEEEEE")
        self.kb.update_cell(x, y, '_')
        self.kb.update_unknown_cell(x, y, '_')
        self.dude.arrows -= 1
        self.cost += 10
        self.dude.killed_wumpii += 1

    # places the explorer in the starting cell, facing south, update percept and tell KnowledgeBase cell is safe
    def place_dude(self):
        self.logger.info("Placing Dude at (0, 0), facing south")
        self.kb.update_cell(0, 0, "v")
        self.kb.update_percept(0, 0)
        self.kb.tell('a', 0, 0)  # 0, 0 is safe

    # upon move, check cell for event, update map and percepts accordingly
    def successful_move(self, x, y, direction):
        self.change_direction(direction)
        # if in square with gold, grab gold
        if self.kb.unknown_map[x][y] == '$':
            self.grab_gold()
            return True
        # don't update percept for square with obstacle
        elif self.kb.unknown_map[x][y] == 'o':
            self.kb.update_cell(x, y, "o")
            self.kb.tell('o', x, y)
            return False
        # if in square with pit, call pit fall handler
        elif self.kb.unknown_map[x][y] == 'p':    
            self.pit_fall()
            self.kb.update_cell(x, y, "p")
            self.kb.tell('p', x, y)
            return False
        # if in square with wumpus, call wumpus handler
        elif self.kb.unknown_map[x][y] == 'w':    
            self.wumpus_encounter()
            self.kb.update_cell(x, y, "w")
            self.kb.tell('w', x, y)
            return False
        else:
            # cell is safe and explored
            self.dude.cells_explored += 1
            self.kb.update_cell(self.dude.prevx, self.dude.prevy, 's')
            self.kb.tell('a', x, y)
        return True

    # Given starting direction and ending direction, turn left or right until correct
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
            self.logger.info("Turning Left")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction])
            self.cost -= 1
        elif direction - current == 1:
            self.logger.info("Turning Right")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction])
            self.cost -= 1
        elif direction - current == -2:
            self.logger.info("Turning Left")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction + 1])
            self.cost -= 1
            self.logger.info("Turning Left")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction])
            self.cost -= 1
        elif direction - current == 2:
            self.logger.info("Turning Right")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction - 1])
            self.cost -= 1
            self.logger.info("Turning Right")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction])
            self.cost -= 1
        elif direction - current == 3:
            self.logger.info("Turning Left")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction])
            self.cost -= 1
        elif direction - current == -3:
            self.logger.info("Turning Right")
            self.kb.update_cell(self.dude.x, self.dude.y, direction_list[direction])
            self.cost -= 1
        else:
            self.logger.info("Got turned around...")

    # End game and update stats
    def grab_gold(self):
        self.logger.info("Gold found!")
        self.moves += 1
        self.cost += 1000
        self.gold_found = True

    # Death and update of stats
    def pit_fall(self):
        self.logger.info("Ahhhhhhhhhhhhhhhhhhhh!")
        self.logger.info("RIP Explorer, you fell into a pit.")
        self.moves += 1
        self.cost -= 1000
        self.dude.death_by_pit += 1

    # Death and update of stats
    def wumpus_encounter(self):
        self.logger.info("Crunch.")        
        self.logger.info("RIP Explorer, you were eaten by a wumpus.")
        self.moves += 1
        self.cost -= 1000
        self.dude.death_by_wumpii += 1

