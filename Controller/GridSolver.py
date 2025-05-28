from abc import ABC, abstractmethod


class GridSolver(ABC):
    def __init__(self):
        self._grid = None
        self._pencil_marks = None
        self._filled_cells = None

    # create pencil marks for the sudoku grid, symbolizing candidates for each cell
    @abstractmethod
    def _create_pencil_marks(self):
        pass

    # insert the value into the cell and update pencil marks
    @abstractmethod
    def _insert_cell(self, y_pos, x_pos, value):
        pass

    # try filling out a space using the "hidden singles" technique
    @abstractmethod
    def _try_hidden_singles(self):
        pass

    # try filling out a space using the "naked singles" technique
    @abstractmethod
    def _try_naked_singles(self):
        pass

    # try eliminating candidates (marks) from cells using the "hidden pairs" technique
    @abstractmethod
    def _try_hidden_pairs(self):
        pass

    # try solving the grid using different methods
    @abstractmethod
    def try_solving(self, grid, filled_cells, difficulty):
        pass
