from RegSudokuGame import RegSudokuGame
from BigSudokuGame import BigSudokuGame
from Difficulty import Difficulty


class GameFactory:
    def __init__(self):
        pass

    def create_a_game(self, solved_grid, solvable_grid, difficulty):
        if difficulty == Difficulty.BIG:
            return BigSudokuGame(solved_grid, solvable_grid)
        else:
            return RegSudokuGame(solved_grid, solvable_grid, difficulty)
