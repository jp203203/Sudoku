from typing import override
from tkinter import *
from tkinter.font import Font
from pynput.keyboard import Key, Listener
import threading
from View.View import View
from View.IGameViewUpdate import IGameViewUpdate
from Controller.IGameInteraction import IGameInteraction
from Model.Difficulty import Difficulty


class SudokuView(View, IGameViewUpdate):
    def __init__(self, game_interaction):
        self._grid = None
        self._hint_img = None
        self._hint_btn = None
        self._mark_img = None
        self._mark_btn = None
        self._mistakes_lbl = None

        self._cell_selected_ids = [[0 for _ in range(9)] for _ in range(9)]
        self._cell_highlighted_ids = [[0 for _ in range(9)] for _ in range(9)]
        self._cell_hitbox_ids = [[0 for _ in range(9)] for _ in range(9)]
        self._cell_value_ids = [[0 for _ in range(9)] for _ in range(9)]
        self._selected_cell = (-1, -1)

        self._marks_on = False

        super().__init__(game_interaction)

        # start a thread for listening for keyboard events
        listener_thread = threading.Thread(target=self._start_listener, daemon=True)
        listener_thread.start()

    @override
    def _create(self):
        # create root of the frame
        self._root = Tk()
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
                                command=lambda: self._get_hint())
        self._hint_btn.grid(row=1, column=0)

        self._mistakes_lbl = Label(self._root, text="mistakes left: ", font=Font(size=17))
        self._mistakes_lbl.grid(row=1, column=1)

        self._mark_img = PhotoImage(file='../assets/pencil.png')
        self._mark_btn = Button(self._root, image=self._mark_img, font=Font(size=30), fg='#2b7eb5')
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

    def _start_listener(self):
        # create a listener object
        with Listener(on_press=self._cell_input) as listener:
            listener.join()

    def _cell_input(self, key):
        # if keys 1-9 are pressed either from keyboard or numpad, insert the respective value into the selected cell
        # if backspace is pressed, remove the value from the selected cell
        # ignore all other keys
        if self._selected_cell[0] != -1 and self._selected_cell[1] != -1:
            if key == Key.backspace:
                self._write_number(0, self._selected_cell[0], self._selected_cell[1], None)
            try:
                if 97 <= key.vk <= 105:
                    self._game_interaction.insert_cell(self._selected_cell[0], self._selected_cell[1], key.vk - 96)
                elif 49 <= key.vk <= 57:
                    self._game_interaction.insert_cell(self._selected_cell[0], self._selected_cell[1], key.vk - 48)
                else:
                    pass
            except AttributeError:
                pass

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

    def _get_hint(self):
        x = self._selected_cell[0]
        y = self._selected_cell[1]
        if x != -1 and y != -1:
            if self._cell_value_ids[y][x] == 0:
                self._game_interaction.get_hint(x, y)
            self._hint_btn["state"] = "disabled"

    # game update interface methods
    @override
    def update_cell(self, x, y, value, correct):
        self._write_number(value, x, y, correct)

    @override
    def update_mistakes(self, mistakes_left):
        pass

    @override
    def finish_game(self, won):
        pass
