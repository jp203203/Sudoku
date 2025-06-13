from abc import ABC, abstractmethod
from Model.SudokuBoard import SudokuBoard


class SudokuGame(ABC):
    _init_mistakes = None
    _size = None

    def __init__(self, solved_grid, solvable_grid, filled_cells, difficulty):
        self._board = SudokuBoard(solved_grid, solvable_grid)
        self._difficulty = difficulty
        self._mistakes_left = None
        self._cells_at_start = filled_cells
        self._filled_cells = self._cells_at_start

    def get_board(self):
        return self._board

    def get_mistakes_left(self):
        return self._mistakes_left

    def get_filled_cells(self):
        return self._filled_cells

    def get_difficulty(self):
        return self._difficulty

    def set_mistakes_left(self, val):
        self._mistakes_left = val

    def set_filled_cells(self, val):
        self._filled_cells = val

    def reset_filled_cells(self):
        self._filled_cells = self._cells_at_start

    @abstractmethod
    def reset_mistakes(self):
        pass

    @abstractmethod
    def get_size(self):
        pass