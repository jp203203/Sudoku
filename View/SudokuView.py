import os
import sys
from typing import override
from tkinter import *
from tkinter.font import Font
from View.View import View
from View.IGameViewUpdate import IGameViewUpdate
from Controller.IGameInteraction import IGameInteraction
from Model.Difficulty import Difficulty


class SudokuView(View, IGameViewUpdate):
    def __init__(self, game_interaction, board_size=9):
        self._grid = None
        self._hint_img = None
        self._hint_btn = None
        self._mark_img = None
        self._mark_btn = None
        self._mistakes_lbl = None

        self._cell_selected_ids = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self._cell_highlighted_ids = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self._cell_hitbox_ids = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self._cell_value_ids = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self._cell_mark_ids = [[[0 for _ in range(board_size)] for _ in range(board_size)] for _ in range(board_size)]
        self._selected_cell = (-1, -1)

        self._marks_on = False

        super().__init__(game_interaction)

    @override
    def _create(self):
        # create root of the frame
        self._root = Tk()
        # add key binding
        self._root.bind("<Key>", self._on_key_press)
        # handle window close event
        self._root.protocol("WM_DELETE_WINDOW", self._game_interaction.new_game)

        self._root.resizable(False, False)
        self._root.title("Sudoku 9x9")
        self._root.geometry('551x600')
        self._root.rowconfigure((0, 1), weight=1)
        self._root.columnconfigure((0, 1, 2), weight=1)

        cell_size = 50

        # create sudoku grid as a canvas
        self._grid = Canvas(self._root, width=453, height=453)
        self._grid.grid(row=0, column=0, columnspan=3)

        # create colored squares for selected and highlighted cells, and hide them
        # additionally create click event listeners as transparent hitboxes
        for row in range(9):
            for cell in range(9):
                x0 = cell_size * cell + 4
                y0 = cell_size * row + 4
                x1 = x0 + 49
                y1 = y0 + 49

                # highlighted cells first
                self._cell_highlighted_ids[row][cell] = self._grid.create_rectangle(x0, y0, x1, y1,
                                                                                    width=0, fill='#b6cdde')
                self._grid.itemconfig(self._cell_highlighted_ids[row][cell], state='hidden')

                # selected cells above highlighted
                self._cell_selected_ids[row][cell] = self._grid.create_rectangle(x0, y0, x1, y1,
                                                                                 width=0, fill='#2b7eb5')
                self._grid.itemconfig(self._cell_selected_ids[row][cell], state='hidden')

                mark_idx = 0
                # create pencil marks
                for mark_row in range(3):
                    for mark_col in range(3):
                        mark_x = x0 + 9 + 16 * mark_col
                        mark_y = y0 + 9 + 16 * mark_row
                        self._cell_mark_ids[row][cell][mark_idx] = self._grid.create_text(
                            mark_x, mark_y,
                            text=str(mark_idx + 1),
                            font=('Helvetica', 10),
                            fill='#4a4a4a'
                        )
                        self._grid.itemconfig(self._cell_mark_ids[row][cell][mark_idx], state='hidden')
                        mark_idx += 1

                # create hitboxes
                self._cell_hitbox_ids[row][cell] = self._grid.create_rectangle(x0, y0, x1, y1,
                                                                               width=0, fill='', outline='')
                self._grid.tag_bind(self._cell_hitbox_ids[row][cell], '<Button-1>',
                                    lambda e, x=cell, y=row: self._select_cells(x, y))

        for i in range(10):
            # add vertical and horizontal lines
            line_width = 3 if i % 3 == 0 else 1
            self._grid.create_line(i * cell_size + 3, 0, i * cell_size + 3, 454, width=line_width)
            self._grid.create_line(0, i * cell_size + 3, 454, i * cell_size + 3, width=line_width)

        # add buttons and a mistakes label
        self._hint_img = PhotoImage(file='../assets/bulb.png')
        self._hint_btn = Button(self._root, image=self._hint_img, font=Font(size=30), fg='#2b7eb5',
                                command=self._get_hint)
        self._hint_btn.grid(row=1, column=0)

        self._mistakes_lbl = Label(self._root, text="mistakes left: ", font=Font(size=17))
        self._mistakes_lbl.grid(row=1, column=1)

        self._mark_img = PhotoImage(file='../assets/pencil.png')
        self._mark_btn = Button(self._root, image=self._mark_img, font=Font(size=30), fg='#2b7eb5',
                                command=self._switch_marks)
        self._mark_btn.grid(row=1, column=2)

    # highlight selected cell and all cells in the same row, column and sub-grid
    def _select_cells(self, x, y):
        # hide previous highlights first
        for i in range(9):
            for j in range(9):
                self._grid.itemconfig(self._cell_highlighted_ids[i][j], state='hidden')
                self._grid.itemconfig(self._cell_selected_ids[i][j], state='hidden')

        # highlight selected cell
        self._grid.itemconfig(self._cell_selected_ids[y][x], state='normal')

        # highlight cells in the same row
        for i in range(9):
            if i != x:
                self._grid.itemconfig(self._cell_highlighted_ids[y][i], state='normal')

        # highlight cells in the same column
        for i in range(9):
            if i != y:
                self._grid.itemconfig(self._cell_highlighted_ids[i][x], state='normal')

        # highlight cells in the same sub-grid
        first_x = (x // 3) * 3
        first_y = (y // 3) * 3

        for i in range(first_y, first_y + 3):
            for j in range(first_x, first_x + 3):
                self._grid.itemconfig(self._cell_highlighted_ids[i][j], state='normal')

        self._selected_cell = (x, y)

    def _write_number(self, value, x, y, correct):
        # determine the position of the value to be inserted
        cell_size = 50
        cell_x = cell_size * x + 29
        cell_y = cell_size * y + 29

        if self._grid is not None:
            # fill the cell if the value is not 0 (key 1-9 pressed)
            if value != 0:
                # if another value is present in the cell, remove it before inserting a new one
                if self._cell_value_ids[y][x] != 0:
                    self._grid.delete(self._cell_value_ids[y][x])

                # choose color depending on input's correctness
                color = ''
                if correct:
                    color = 'black'
                else:
                    color = 'red'

                self._cell_value_ids[y][x] = self._grid.create_text(
                    cell_x, cell_y,
                    text=str(value),
                    font=('Helvetica', 24),
                    fill=color
                )

                if correct:
                    # if correct, remove the hitbox and reset the selected cell
                    self._grid.delete(self._cell_hitbox_ids[y][x])
                    self._selected_cell = (-1, -1)
                else:
                    # if not correct, move the text below the hitbox, so that it's not covered by the text
                    self._grid.tag_lower(self._cell_value_ids[y][x],
                                         self._cell_hitbox_ids[y][x])

            # remove the value from the cell if it's not empty, and the value is 0 (backspace pressed)
            if self._cell_value_ids[y][x] != 0 and value == 0:
                self._grid.delete(self._cell_value_ids[y][x])
                self._cell_value_ids[y][x] = 0

            # additionally hide all marks, no matter the input
            for i in range(9):
                self._grid.itemconfig(self._cell_mark_ids[y][x][i], state='hidden')

            # update the marks if inserted value is correct
            if correct:
                self._update_marks(x, y, value)

    def _mark_cell(self, x, y, value):
        if self._grid.itemcget(self._cell_mark_ids[y][x][value - 1], "state") == 'normal':
            self._grid.itemconfig(self._cell_mark_ids[y][x][value - 1], state='hidden')
        else:
            self._grid.itemconfig(self._cell_mark_ids[y][x][value - 1], state='normal')

    def _on_key_press(self, event):
        if self._selected_cell[0] != -1 and self._selected_cell[1] != -1:
            x = self._selected_cell[0]
            y = self._selected_cell[1]

            if self._marks_on:
                action = self._mark_cell
            else:
                action = self._game_interaction.insert_cell

            if event.keysym == "BackSpace":
                self._write_number(0, x, y, None)
            elif event.char.isdigit():
                value = int(event.char)
                if 1 <= value <= 9:
                    action(x, y, value)
            elif event.char.upper() == 'W':
                self._game_interaction.win()
    def _update_marks(self, x, y, value):
        # remove the marks from correct spot
        for i in range(9):
            self._grid.delete(self._cell_mark_ids[y][x][i])

        # hide pencil marks for the same row
        for col_idx in range(9):
            if col_idx != x:
                self._grid.itemconfig(self._cell_mark_ids[y][col_idx][value-1], state='hidden')

        # hide pencil marks for the same column
        for row_idx in range(9):
            if row_idx != y:
                self._grid.itemconfig(self._cell_mark_ids[row_idx][x][value-1], state='hidden')

        first_x = (x // 3) * 3
        first_y = (y // 3) * 3

        for row_idx in range(first_y, first_y + 3):
            for col_idx in range(first_x, first_x + 3):
                if not (row_idx == y and col_idx == x):
                    self._grid.itemconfig(self._cell_mark_ids[row_idx][col_idx][value-1], state='hidden')

    def _get_hint(self):
        # get selected cell coordinates
        x = self._selected_cell[0]
        y = self._selected_cell[1]

        # if any cell is selected, get hint from controller and disable the hint button (only one hint per game allowed)
        if x != -1 and y != -1:
            self._game_interaction.get_hint(x, y)
            self._hint_btn["state"] = 'disabled'

    def _switch_marks(self):
        # turn on the option to write pencil marks
        self._marks_on = not self._marks_on
        # change the button color depending on the option activity
        if self._marks_on:
            self._mark_btn.config(bg='#828282', activebackground='#828282')
        else:
            self._mark_btn.config(bg=self._root.cget("bg"), activebackground=self._root.cget("bg"))

    # game update interface methods
    @override
    def update_cell(self, x, y, value, correct):
        self._write_number(value, x, y, correct)

    @override
    def update_mistakes(self, mistakes_left):
        self._mistakes_lbl.config(text="mistakes left: " + str(mistakes_left))

    @override
    def lock_game(self):
        # hide all hitboxes so they can't be clicked on
        for row in self._cell_hitbox_ids:
            for cell in row:
                self._grid.itemconfig(cell, state='hidden')

        # unselect any selected cell
        self._selected_cell = (-1, -1)

        # disable buttons
        self._hint_btn["state"] = 'disabled'
        self._mark_btn["state"] = 'disabled'
