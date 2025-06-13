class SudokuBoard:
    def __init__(self, solved_grid, solvable_grid):
        self._solved_grid = solved_grid
        self._solvable_grid = solvable_grid

    def get_solved_grid(self):
        return self._solved_grid

    def get_solvable_grid(self):
        return self._solvable_grid

    def print_board(self):
        for row in self._solvable_grid:
            for cell in row:
                print(cell, end=" ")
            print("\n", end="")
