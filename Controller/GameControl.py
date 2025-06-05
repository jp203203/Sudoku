from typing import override
from IGameInteraction import IGameInteraction
from View.MenuView import MenuView
from View.SudokuView import SudokuView
from View.BigSudokuView import BigSudokuView
from Model.Difficulty import Difficulty
from Controller.BigGameGenerator import BigGameGenerator
from Controller.RegGameGenerator import RegGameGenerator


class GameControl(IGameInteraction):
    def __init__(self):
        super().__init__()
        self._view = None
        self._game = None
        self._game_generator = None

    def main(self):
        # create and display the menu (difficulty choice) view
        self._view = MenuView(self)
        self._view.start()

    def _play_game(self, difficulty):
        if difficulty == Difficulty.BIG:
            self._game_generator = BigGameGenerator()
        else:
            self._game_generator = RegGameGenerator()

        self._game = self._game_generator.generate_game(difficulty)

        if difficulty == Difficulty.BIG:
            self._view = BigSudokuView(self)
        else:
            self._view = SudokuView(self)

        # insert all cells which are already filled
        for y in range(9):
            for x in range(9):
                cell_val = self._game.get_board().get_solvable_grid()[y][x]
                if cell_val != 0:
                    self._view.update_cell(x, y, cell_val, True)

        # display the game view
        self._view.start()

    # game interaction interface methods
    @override
    def choose_difficulty(self, difficulty):
        self._play_game(difficulty)

    @override
    def pencil_mark(self, x, y, value):
        pass

    @override
    def insert_cell(self, x, y, value):
        correct = (self._game.get_board().get_solved_grid()[y][x] == value)
        self._view.update_cell(x, y, value, correct)

    @override
    def get_hint(self, x, y):
        cell_val = self._game.get_board().get_solved_grid()[y][x]
        self._view.update_cell(x, y, cell_val, True)


if __name__ == '__main__':
    game_control = GameControl()
    game_control.main()
