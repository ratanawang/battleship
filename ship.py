import random as r


def pick_orientation():
    if r.randint(0, 1) == 0:
        return "v"
    return "h"


def pick_direction(orientation):
    rand = r.randint(0, 1)
    if orientation == "v":
        if rand == 0:
            return "up"
        return "down"
    elif orientation == "h":
        if rand == 0:
            return "left"
        return "right"


class Ship:

    name = ""
    length = 0
    cells_occupied = []
    status = ""
    dir = ""
    start_cell = ""

    def __init__(self, type):
        self.name = type
        if type == "destroyer":
            self.length = 2
        elif type == "submarine" or type == "cruiser":
            self.length = 3
        elif type == "battleship":
            self.length = 4
        elif type == "carrier":
            self.length = 5
        self.status = f"{self.length}/{self.length}"
        self.choose_direction()
        self.cells_occupied = []

    def print_status(self):
        print(self.status)

    def track_cells_occupied(self, row, col):
        self.cells_occupied.append(f"{row},{col}")

    def delete_cell(self, row, col):
        self.cells_occupied.remove(f"{row},{col}")
        if len(self.cells_occupied) == 0:
            print("The {} has sunk!".format(self.name))
        self.status = str(int(self.status[0]) - 1) + self.status[1:]

    def choose_direction(self):
        self.dir = pick_direction(pick_orientation())

    def flip_direction(self):
        if self.dir == "up":
            self.dir = "down"
        elif self.dir == "down":
            self.dir = "up"
        elif self.dir == "left":
            self.dir = "right"
        elif self.dir == "right":
            self.dir = "left"

    def get_direction(self):
        return self.dir

    def save_start_cell(self, row, col):
        self.start_cell = f"{row},{col}"
