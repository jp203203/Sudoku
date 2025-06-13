import sys
from typing import override
from IGameInteraction import IGameInteraction
from View.ViewFactory import ViewFactory
from Model.Difficulty import Difficulty
from Controller.BigGameGenerator import BigGameGenerator
from Controller.RegGameGenerator import RegGameGenerator


class GameControl(IGameInteraction):
    def __init__(self):
        super().__init__()
        self._view_factory = None
        self._view = None
        self._game = None
        self._game_generator = None

    def main(self):
        # create and display the menu (difficulty choice) view
        self._view_factory = ViewFactory(self)
        self._view = self._view_factory.create_view("menu")
        self._view.start()

    def _create_game(self, difficulty):
        if difficulty == Difficulty.BIG:
            self._game_generator = BigGameGenerator()
        else:
            self._game_generator = RegGameGenerator()

        self._game = None  # deletes the previous game
        while self._game is None:
            self._game = self._game_generator.generate_game(difficulty)  # creates a new one

    def _play_game(self):
        if self._game.get_difficulty() == Difficulty.BIG:
            self._view = self._view_factory.create_view("bigsudoku")
        else:
            self._view = self._view_factory.create_view("sudoku")

        # insert all cells which are already filled
        board_size = self._game.get_size()
        for y in range(board_size):
            for x in range(board_size):
                cell_val = self._game.get_board().get_solvable_grid()[y][x]
                if cell_val != 0:
                    self._view.update_cell(x, y, cell_val, True)

        self._view.update_mistakes(self._game.get_mistakes_left())

        # display the game view
        self._view.start()

    def _display_end_game_view(self, won):
        if won:
            end_view = self._view_factory.create_view("win")
            end_view.start()
        else:
            end_view = self._view_factory.create_view("loss")
            end_view.start()

    # game interaction interface methods
    @override
    def choose_difficulty(self, difficulty):
        self._view.get_root().destroy()  # destroy the menu view's root
        self._create_game(difficulty)
        self._play_game()  # start the game

    @override
    def insert_cell(self, x, y, value):
        correct = (self._game.get_board().get_solved_grid()[y][x] == value)
        self._view.update_cell(x, y, value, correct)

        # update the mistakes left count if guess was incorrect
        if not correct:
            self._game.set_mistakes_left(self._game.get_mistakes_left() - 1)
            self._view.update_mistakes(self._game.get_mistakes_left())

            # if no mistakes to make left, lock the game and display the window with appropriate message
            if self._game.get_mistakes_left() == 0:
                self._view.lock_game()
                self._display_end_game_view(False)

        # update the filled cells count if guess was correct
        else:
            self._game.set_filled_cells(self._game.get_filled_cells() + 1)

            # if all cells were filled, lock the game and display the window with appropriate message
            if self._game.get_filled_cells() == self._game.get_size() ** 2:
                self._view.lock_game()
                self._display_end_game_view(True)

    @override
    def get_hint(self, x, y):
        cell_val = self._game.get_board().get_solved_grid()[y][x]
        self._view.update_cell(x, y, cell_val, True)

        # update filled cells count
        self._game.set_filled_cells(self._game.get_filled_cells() + 1)

        # if all cells were filled, lock the game and display the window with appropriate message
        if self._game.get_filled_cells() == self._game.get_size() ** 2:
            self._view.lock_game()
            self._display_end_game_view(True)

    @override
    def new_game(self):
        # destroy the previous game view's root
        self._view.get_root().destroy()
        # create new menu view
        self._view = self._view_factory.create_view("menu")
        self._view.start()

    @override
    def retry(self):
        # reset mistakes and filled cells
        self._game.reset_mistakes()
        self._game.reset_filled_cells()

        # destroy the previous game view's root
        self._view.get_root().destroy()  # PROGRAM TERMINATES HERE
        # play the game again (without creating new one)
        self._play_game()

    @override
    def terminate(self):
        sys.exit()

    @override
    def win(self):
        size = self._game.get_size()

        for i in range(size):
            for j in range(size):
                if self._game.get_board().get_solvable_grid()[j][i] == 0:
                    value = self._game.get_board().get_solved_grid()[j][i]
                    self._view.update_cell(i, j, value, True)

                    self._game.set_filled_cells(self._game.get_filled_cells() + 1)

        self._view.lock_game()
        self._display_end_game_view(True)


if __name__ == '__main__':
    game_control = GameControl()
    game_control.main()
