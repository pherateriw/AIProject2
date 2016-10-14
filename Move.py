# TODO not pass kb in all methods?

def move_direction(kb, x, y, direction):
    if direction == "NORTH":
        print("Moving North")
        temp = x
        temp -= 1
        if successful_move(kb, temp, y):
            kb.update_cell(x, y, "_")
            x -= temp
    if direction == "SOUTH":
        print("Moving South")
        temp = x
        temp += 1
        if successful_move(kb, temp, y):
            kb.update_cell(x, y, "_")
            x = temp
    if direction == "EAST":
        print("Moving East")
        temp = y
        temp += 1
        if successful_move(kb, x, temp):
            kb.update_cell(x, y, "_")
            y = temp
    if direction == "WEST":
        print("Moving West")
        temp = y
        temp -= 1
        if successful_move(kb, x, temp):
            kb.update_cell(x, y, "_")
            y = temp
    kb.update_cell(x, y, "D")
    return x, y


def place_dude(kb):
    print("Placing Dude at (0, 0)")
    kb.update_cell(0, 0, "D")


def successful_move(kb, x, y):
    if kb.unknown_map[x][y] == 'o':
        print("Thunk!")
        kb.update_cell(x, y, "o")
        return False
    return True