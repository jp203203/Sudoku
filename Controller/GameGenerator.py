from abc import ABC, abstractmethod


class GameGenerator(ABC):
    def __init__(self):
        self._full_grid = None
        self._solvable_grid = None
        self._solvable_grid_copy = None
        self._solver = None

    # backtracking algorithm for creating valid sudoku solutions
    @abstractmethod
    def _backtrack_fill(self, x, y):
        pass

    # generates full grid using backtracking algorithm
    @abstractmethod
    def _generate_full_grid(self):
        pass

    # generates solvable grid based on the full grid
    @abstractmethod
    def _generate_solvable_grid(self, difficulty):
        pass

    # creates a new sudoku game
    @abstractmethod
    def generate_game(self, difficulty):
        pass
