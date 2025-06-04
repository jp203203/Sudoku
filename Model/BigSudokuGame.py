from typing import override
from Model.SudokuGame import SudokuGame


class BigSudokuGame(SudokuGame):
    def __init__(self, solved_grid, solvable_grid):
        super().__init__(solved_grid, solvable_grid)
        self._pencil_marks = [[[False for _ in range(16)] for _ in range(16)] for _ in range(16)]
        self._mistakes_left = 5
        pass

    @override
    def set_pencil_mark(self, x, y, val):
        self._pencil_marks[y][x][val] = not self._pencil_marks[y][x][val]
