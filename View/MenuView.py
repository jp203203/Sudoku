from typing import override
from tkinter import *
from tkinter.font import Font
from View.View import View
from Controller.IGameInteraction import IGameInteraction
from Model.Difficulty import Difficulty


class MenuView(View):
    def __init__(self, game_interaction):
        super().__init__(game_interaction)

    @override
    def _create(self):
        # create root of the frame
        self._root = Tk()
        self._root.resizable(False, False)

        self._root.title("Welcome to Sudoku!")
        self._root.geometry('350x300')

        # handle window close event
        self._root.protocol("WM_DELETE_WINDOW", self._close)

        # add prompt label
        difficulty_prompt_lbl = Label(self._root, text="Choose difficulty:", font=Font(size=15, weight="bold"))
        difficulty_prompt_lbl.place(relx=0.5, rely=0.1, anchor=CENTER)

        # add button frame for choosing difficulty
        btn_frame = Frame(self._root)
        btn_frame.grid(rowspan=4, columnspan=1)

        easy_btn = Button(btn_frame, text='Easy', font=Font(size=10, weight="bold"), fg="green",
                          height=2, width=35, activebackground="green", activeforeground="white",
                          command=lambda: self._game_interaction.choose_difficulty(Difficulty.EASY))
        medium_btn = Button(btn_frame, text='Medium', font=Font(size=10, weight="bold"), fg="orange",
                            height=2, width=35, activebackground="orange", activeforeground="white",
                            command=lambda: self._game_interaction.choose_difficulty(Difficulty.MEDIUM))
        hard_btn = Button(btn_frame, text='Hard', font=Font(size=10, weight="bold"), fg="red",
                          height=2, width=35, activebackground="red", activeforeground="white",
                          command=lambda: self._game_interaction.choose_difficulty(Difficulty.HARD))
        big_btn = Button(btn_frame, text='Big (16x16)', font=Font(size=10, weight="bold"), fg="purple",
                         height=2, width=35, activebackground="purple", activeforeground="white",
                         command=lambda: self._game_interaction.choose_difficulty(Difficulty.BIG))

        easy_btn.grid(row=0, column=0, pady=(10, 0))
        medium_btn.grid(row=1, column=0, pady=(10, 0))
        hard_btn.grid(row=2, column=0, pady=(10, 0))
        big_btn.grid(row=3, column=0, pady=(10, 0))
        btn_frame.place(relx=0.5, rely=0.2, anchor=N)
