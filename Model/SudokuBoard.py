class SudokuBoard:
    def __init__(self, solved_grid, solvable_grid):
        self._solved_board = solved_grid
        self._solvable_board = solvable_grid
        pass

    def get_solved_grid(self):
        return self._solved_board

    def get_solvable_grid(self):
        return self._solvable_board
