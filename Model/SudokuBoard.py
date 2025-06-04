class SudokuBoard:
    def __init__(self, solved_grid, solvable_grid):
        self._solved_board = solved_grid
        self._solvable_board = solvable_grid
        pass

    def get_solved_grid(self):
        return self._solved_board

    def get_solvable_grid(self):
        return self._solvable_board

    def print_board(self):
        for row in self._solvable_board:
            for cell in row:
                print(cell, end=" ")
            print("\n", end="")