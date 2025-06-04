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
        self._view = MenuView(self)

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

    @override
    def choose_difficulty(self, difficulty):
        print("Selected difficulty", difficulty.name, sep=" ", end="\n")

        self._play_game(difficulty)

    @override
    def pencil_mark(self, x, y, value):
        pass

    @override
    def fill_cell(self, x, y, value):
        pass


if __name__ == '__main__':
    game_control = GameControl()
    game_control.main()
