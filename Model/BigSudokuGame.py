from Model.SudokuGame import SudokuGame


class BigSudokuGame(SudokuGame):
    def __init__(self, solved_grid, solvable_grid, filled_cells):
        super().__init__(solved_grid, solvable_grid, filled_cells)
        self._pencil_marks = [[[False for _ in range(16)] for _ in range(16)] for _ in range(16)]
        self._mistakes_left = 4
