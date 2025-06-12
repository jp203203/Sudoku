from View.MenuView import MenuView
from View.SudokuView import SudokuView
from View.BigSudokuView import BigSudokuView
from View.WinView import WinView
from View.LossView import LossView


class ViewFactory:
    def __init__(self, game_interaction):
        self._game_interaction = game_interaction

    def create_view(self, view_type):
        match view_type:
            case "menu":
                return MenuView(self._game_interaction)
            case "sudoku":
                return SudokuView(self._game_interaction)
            case "bigsudoku":
                return BigSudokuView(self._game_interaction)
            case "win":
                return WinView(self._game_interaction)
            case "loss":
                return LossView(self._game_interaction)
            case _:
                raise ValueError("Wrong view type (view_type) passed as an argument")
