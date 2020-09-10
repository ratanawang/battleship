import ship as s
import board as b
import random as r


def place_ship(sh, board, comp):
    if comp:
        row_col = pick_start_cell(board, sh).split(",")
    else:
        row_col = sh.start_cell.split(",")
    row = int(row_col[0])
    col = int(row_col[1])
    success = ""
    while len(sh.cells_occupied) < sh.length:
        success = find_next_cell(row, col, board, comp, sh)
        if success == "failure":
            break
        rc = sh.cells_occupied[-1].split(",")
        row = int(rc[0])
        col = int(rc[1])
    if success == "success" and not comp:
        print(f"Successfully placed ship: {sh.name}!")


def pick_start_cell(board, sh):
    # pick (row, col) coordinate
    row = r.randint(1, 10)
    col = r.randint(1, 10)
    while not no_collision(row, col, board):
        row = r.randint(1, 10)
        col = r.randint(1, 10)
    board.board[row][col] = "   ∆"
    sh.track_cells_occupied(row, col)
    return f"{row},{col}"


def no_collision(row, col, board):
    if board.board[row][col] == "  []":
        return True
    else:
        return False


def in_bounds(row, col):
    if 11 > row >= 0 and 11 > col >= 0:
        return True
    return False


def valid_coord():
    while True:
        start_cell = input("Enter a starting cell (ie. B5) for your {}. --> ".format(p_ship.name))
        try:
            let = start_cell[0].capitalize()
            num = int(start_cell[1:])
            if let in partial_alphabet and 1 <= num <= 10:
                break
        except Exception:
            print("Sorry, that is an invalid starting cell. Please try again.")
    return f"{let},{num}"


def find_next_cell(row, col, board, comp, sh):
    if sh.get_direction() == "up":
        temp_row = row - 1
        if not in_bounds(temp_row, col):
            temp_row += 1
            sh.flip_direction()
            while board.board[temp_row][col] == "   ∆":
                temp_row += 1
        if no_collision(temp_row, col, board):
            board.occupy_cell(temp_row, col)
            sh.track_cells_occupied(temp_row, col)
            return "success"
        else:
            # ship does not fit into the selected cells
            try_again(sh, board, comp)
            return "failure"
    elif sh.get_direction() == "down":
        temp_row = row + 1
        if not in_bounds(temp_row, col):
            temp_row -= 1
            sh.flip_direction()
            while board.board[temp_row][col] == "   ∆":
                temp_row -= 1
        if no_collision(temp_row, col, board):
            board.occupy_cell(temp_row, col)
            sh.track_cells_occupied(temp_row, col)
            return "success"
        else:
            # ship does not fit into the selected cells
            try_again(sh, board, comp)
            return "failure"
    elif sh.get_direction() == "left":
        temp_col = col - 1
        if not in_bounds(row, temp_col):
            temp_col += 1
            sh.flip_direction()
            while board.board[row][temp_col] == "   ∆":
                temp_col += 1
        if no_collision(row, temp_col, board):
            board.occupy_cell(row, temp_col)
            sh.track_cells_occupied(row, temp_col)
            return "success"
        else:
            # ship does not fit into the selected cells
            try_again(sh, board, comp)
            return "failure"
    elif sh.get_direction() == "right":
        temp_col = col + 1
        if not in_bounds(row, temp_col):
            temp_col -= 1
            sh.flip_direction()
            while board.board[row][temp_col] == "   ∆":
                temp_col -= 1
        if no_collision(row, temp_col, board):
            board.occupy_cell(row, temp_col)
            sh.track_cells_occupied(row, temp_col)
            return "success"
        else:
            # ship does not fit into the selected cells
            try_again(sh, board, comp)
            return "failure"


def delete_ship_from_board(sh, board):
    for coord in sh.cells_occupied:
        rc = coord.split(",")
        board.board[int(rc[0])][int(rc[1])] = "  []"
    sh.cells_occupied = []


def place_player_ship(sh, board):
    rc = valid_coord().split(",")
    start_row = partial_alphabet.index(rc[0])
    start_col = int(rc[1])
    sh.track_cells_occupied(start_row, start_col)
    board.board[start_row][start_col] = "   ∆"
    sh.save_start_cell(start_row, start_col)
    valid_directions = "up down left right"
    ship_dir = "0"
    while ship_dir not in valid_directions:
        ship_dir = input("In which the direction is the ship facing? (up/down/left/right) --> ")
        if ship_dir not in valid_directions:
            print("Sorry, that is an invalid direction. Please try again.")
    sh.dir = ship_dir
    place_ship(sh, player_board, False)
    player_board.print_board()


def try_again(sh, board, comp):
    delete_ship_from_board(sh, board)
    if comp:
        place_ship(sh, board, comp)
    else:
        print("Sorry, you can't place your ship here. Please pick different cells.")
        # restart player picking cells process
        place_player_ship(sh, board)


def play(board, comp, row=0, col=0):
    if comp and row != 0 and col != 0:
        pass
    elif comp and row == 0 and col == 0:  # default values
        row = r.randint(1, 10)
        col = r.randint(1, 10)
        if vis_comp_board.board[row][col] != "   •" and vis_comp_board.board[row][col] != "   X":
            print("Computer fires at {}{}!".format(partial_alphabet[row], col))
            hit_or_miss(row, col, board, comp)
        else:
            play(board, comp)
    elif not comp and row != 0 and col != 0:
        if vis_board.board[row][col] != "   •" and vis_board.board[row][col] != "   X":
            print("You fire at {}{}!".format(partial_alphabet[row], col))
            hit_or_miss(row, col, board, comp)


def hit_or_miss(row, col, board, comp):
    if board.board[row][col] == "   ∆":
        print("HIT! {}{} is down.".format(partial_alphabet[row], col))
        winner = True
        if comp:
            for sh in player_ships:
                if f"{row},{col}" in sh.cells_occupied:
                    sh.delete_cell(row, col)
            vis_comp_board.board[row][col] = "   X"
            for sh in player_ships:
                if len(sh.cells_occupied) != 0:
                    winner = False
        else:
            for sh in comp_ships:
                if f"{row},{col}" in sh.cells_occupied:
                    sh.delete_cell(row, col)
            vis_board.board[row][col] = "   X"
            for sh in comp_ships:
                if len(sh.cells_occupied) != 0:
                    winner = False
        if winner:
            win(comp)
        rc = choose_next_target(board, comp).split(",")
        play(board, comp, int(rc[0]), int(rc[1]))
    elif board.board[row][col] == "  []":
        print("MISS! Better luck next time.")
        if comp:
            vis_comp_board.board[row][col] = "   •"
        else:
            vis_board.board[row][col] = "   •"
    if comp:
        vis_comp_board.print_board()
    else:
        vis_board.print_board()


def win(comp):
    if comp:
        print("Oops, you lose.")
    else:
        print("Congratulations! You win.")


def choose_next_target(board, comp):
    if comp:
        play(board, comp)
        return "0,0"
        # temp_row = 0
        # temp_col = 0
        # while not in_bounds(temp_row, temp_col):
        #     comp_dir = s.pick_direction(s.pick_orientation())
        #     temp_row = row
        #     temp_col = col
        #     if comp_dir == "up":
        #         temp_row -= 1
        #     elif comp_dir == "down":
        #         temp_row += 1
        #     elif comp_dir == "left":
        #         temp_col -= 1
        #     elif comp_dir == "right":
        #         temp_col += 1
        # if vis_comp_board.board[temp_row][temp_col] == "   •" or vis_comp_board.board[temp_row][temp_col] == "   X":
    else:
        rc = valid_coord().split(",")
        row = partial_alphabet.index(rc[0])
        col = int(rc[1])
        return f"{row},{col}"


# general variables
ship_types = ["destroyer", "submarine", "cruiser", "battleship", "carrier"]
partial_alphabet = "_ABCDEFGHIJ"

# initializes computer board and ships
comp_board = b.Board()
# comp_board.print_board()
comp_ships = []
vis_board = b.Board()
vis_comp_board = b.Board()

for x in range(5):
    ship = s.Ship(ship_types[x])
    comp_ships.append(ship)

for c_ship in comp_ships:
    place_ship(c_ship, comp_board, True)
    # comp_board.print_board()

# START: main menu
while True:
    print("\n"
          "--- Battleship ---\n"
          "* Enter 'start' to begin\n"
          "* Enter 'rules' to see game rules\n"
          "* Enter 'quit' to exit the game\n")
    ui = input()
    if ui == "start":
        break
    elif ui == "rules":
        print("\n"
              "--- Rules ---\n"
              "You have five ships of varying lengths: the destroyer, \n"
              "the submarine, the cruiser, the battleship, and the carrier.\n"
              "You must place your ships and try and sink the enemy's ships\n"
              "while the enemy attempts to sink your ships.\n"
              "\n"
              "[] = empty cell\n"
              "∆ = ship\n"
              "• = hit and miss\n"
              "X = hit and sink\n")
    elif ui == "quit":
        exit()
    else:
        print("unknown command, please try again")

print()
print("Place the ships anywhere on the grid below: \n")

# initializes player board and ships
player_board = b.Board()
player_board.print_board()
print()
player_ships = []

for x in range(5):
    ship = s.Ship(ship_types[x])
    player_ships.append(ship)

for p_ship in player_ships:
    place_player_ship(p_ship, player_board)

# start game
print()
print("--- GAME START ---")
print()
count = 1

while True:
    if count % 2 != 0:  # odd count
        print("Your turn!")
        vis_board.print_board()
        rowcol = valid_coord().split(",")
        ro = partial_alphabet.index(rowcol[0])
        co = int(rowcol[1])
        play(comp_board, False, ro, co)
    else:
        print("Computer's turn!")
        vis_comp_board.print_board()
        play(player_board, True)
    count += 1
