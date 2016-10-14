# TODO not pass kb in all methods?


def move_direction(kb, x, y, direction):
    kb.update_cell(x, y, "_")

    if direction == "NORTH":
        print("Moving North")
        x -= 1
    if direction == "SOUTH":
        print("Moving South")
        x += 1
    if direction == "EAST":
        print("Moving East")
        y += 1
    if direction == "WEST":
        print("Moving West")
        y -= 1

    kb.update_cell(x, y, "D")
    return x, y


def place_dude(kb):
    print("Placing Dude at (0, 0)")
    kb.update_cell(0, 0, "D")
