from abc import ABC, abstractmethod
from SudokuBoard import SudokuBoard


class SudokuGame(ABC):
    def __init__(self, solved_grid, solvable_grid):
        self._board = SudokuBoard(solved_grid, solvable_grid)
        self._hint_used = False
        self._pencil_marks = None
        self._mistakes_left = None
        pass

    def get_board(self):
        return self._board

    def get_pencil_marks(self):
        return self._pencil_marks

    def hint_used(self):
        return self._hint_used

    def get_mistakes_left(self):
        return self._mistakes_left

    @abstractmethod
    def set_pencil_mark(self, x, y, val):
        pass

    def use_hint(self):
        self._hint_used = True

    def set_mistakes_left(self, val):
        self._mistakes_left = val
