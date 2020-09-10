class Board:

    board = []

    def __init__(self):
        # initializes 10 x 10 grid
        self.board = [["  []" for i in range(11)] for j in range(11)]
        self.board[0][0] = " "
        for x in range(1, 11):
            self.board[0][x] = "   " + str(x)
        partial_alphabet = "_ABCDEFGHIJ"
        for y in range(1, 11):
            self.board[y][0] = partial_alphabet[y]

    def print_board(self):
        for x in self.board:
            for y in range(11):
                print(x[y], end=" ")
            print()

    def occupy_cell(self, row, col):
        self.board[row][col] = "   ∆"

