from typing import override
from Model.SudokuGame import SudokuGame


class BigSudokuGame(SudokuGame):
    _init_mistakes = 4

    def __init__(self, solved_grid, solvable_grid, filled_cells, difficulty):
        super().__init__(solved_grid, solvable_grid, filled_cells, difficulty)
        self._mistakes_left = BigSudokuGame._init_mistakes

    @override
    def reset_mistakes(self):
        self._mistakes_left = BigSudokuGame._init_mistakes
