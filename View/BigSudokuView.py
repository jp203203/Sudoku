from typing import override
import tkinter as tk
from tkinter import *
from tkinter.font import Font
from View.View import View
from View.SudokuView import SudokuView
from Controller.IGameInteraction import IGameInteraction
from Model.Difficulty import Difficulty


class BigSudokuView(SudokuView):
    def __init__(self, game_interaction):
        super().__init__(game_interaction)
