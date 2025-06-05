from abc import ABC
from Model.SudokuBoard import SudokuBoard


class SudokuGame(ABC):
    def __init__(self, solved_grid, solvable_grid, filled_cells):
        self._board = SudokuBoard(solved_grid, solvable_grid)
        self._pencil_marks = None
        self._mistakes_left = None
        self._cells_at_start = filled_cells
        self._filled_cells = self._cells_at_start

    def get_board(self):
        return self._board

    def get_pencil_marks(self):
        return self._pencil_marks

    def get_mistakes_left(self):
        return self._mistakes_left

    def get_filled_cells(self):
        return self._filled_cells

    def get_cells_at_start(self):
        return self._cells_at_start

    def set_pencil_mark(self, x, y, val):
        self._pencil_marks[y][x][val] = not self._pencil_marks[y][x][val]

    def set_mistakes_left(self, val):
        self._mistakes_left = val

    def set_filled_cells(self, val):
        self._filled_cells = val
