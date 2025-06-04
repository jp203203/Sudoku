from typing import override
from Model.SudokuGame import SudokuGame
from Model.Difficulty import Difficulty


class RegSudokuGame(SudokuGame):
    def __init__(self, solved_grid, solvable_grid, difficulty):
        super().__init__(solved_grid, solvable_grid)
        self._difficulty = difficulty
        self._pencil_marks = [[[False for _ in range(9)] for _ in range(9)] for _ in range(9)]
        match self._difficulty:
            case Difficulty.EASY:
                self._mistakes_left = 1
            case Difficulty.MEDIUM:
                self._mistakes_left = 2
            case Difficulty.HARD:
                self._mistakes_left = 3
            case _:
                self._mistakes_left = 3
        pass

    @override
    def set_pencil_mark(self, x, y, val):
        self._pencil_marks[y][x][val] = not self._pencil_marks[y][x][val]
