from typing import override
from Model.SudokuGame import SudokuGame
from Model.Difficulty import Difficulty


class RegSudokuGame(SudokuGame):
    _init_mistakes = 3
    _size = 9

    def __init__(self, solved_grid, solvable_grid, filled_cells, difficulty):
        super().__init__(solved_grid, solvable_grid, filled_cells, difficulty)
        self._difficulty = difficulty
        self._mistakes_left = RegSudokuGame._init_mistakes

    @override
    def reset_mistakes(self):
        self._mistakes_left = RegSudokuGame._init_mistakes

    @override
    def get_size(self):
        return RegSudokuGame._size
