from typing import override
from tkinter import *
from tkinter.font import Font
from View.View import View
from Controller.IGameInteraction import IGameInteraction


class WinView(View):
    def __init__(self, game_interaction):
        super().__init__(game_interaction)

    @override
    def _create(self):
        # create root of the frame
        self._root = Tk()
        self._root.resizable(False, False)

        self._root.title("Game won!")
        self._root.geometry('230x120')
        self._root.rowconfigure((0, 1), weight=1)
        self._root.columnconfigure(0, weight=1)

        # handle window close event
        self._root.protocol("WM_DELETE_WINDOW", self._close)

        # create message label
        win_message_lbl = Label(self._root, text="You won the game!", font=Font(size=15, weight='bold'))
        win_message_lbl.grid(row=0, column=0)

        # create new game button
        new_game_btn = Button(self._root, text="new game", command=lambda:
                              [self._root.destroy(), self._game_interaction.new_game()])
        new_game_btn.grid(row=1, column=0)

