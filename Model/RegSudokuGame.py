from Model.SudokuGame import SudokuGame
from Model.Difficulty import Difficulty


class RegSudokuGame(SudokuGame):
    def __init__(self, solved_grid, solvable_grid, filled_cells, difficulty):
        super().__init__(solved_grid, solvable_grid, filled_cells)
        self._difficulty = difficulty
        self._pencil_marks = [[[False for _ in range(9)] for _ in range(9)] for _ in range(9)]
        self._mistakes_left = self._difficulty.value[1]
