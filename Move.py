# TODO not pass kb in all methods?

class Move:

    def __init__(self, kb):
        self.gold_found = False
        self.kb = kb

    def move_direction(self, x, y, direction):
        if direction == "NORTH":
            print("Moving North")
            temp = x
            temp -= 1
            if self.successful_move(temp, y):
                self.kb.update_cell(x, y, "_")
                x = temp
        if direction == "SOUTH":
            print("Moving South")
            temp = x
            temp += 1
            if self.successful_move(temp, y):
                self.kb.update_cell(x, y, "_")
                x = temp
        if direction == "EAST":
            print("Moving East")
            temp = y
            temp += 1
            if self.successful_move(x, temp):
                self.kb.update_cell(x, y, "_")
                y = temp
        if direction == "WEST":
            print("Moving West")
            temp = y
            temp -= 1
            if self.successful_move(x, temp):
                self.kb.update_cell(x, y, "_")
                y = temp
        self.kb.update_cell(x, y, "D")
        return x, y, self.gold_found

    def place_dude(self):
        print("Placing Dude at (0, 0)")
        self.kb.update_cell(0, 0, "D")

    def successful_move(self, x, y):
        if self.kb.unknown_map[x][y] == 'g':
            print("Gold found!")
            self.gold_found = True
            return True
        elif self.kb.unknown_map[x][y] == 'o':
            print("Thunk!")
            self.kb.update_cell(x, y, "o")
            return False
        return True