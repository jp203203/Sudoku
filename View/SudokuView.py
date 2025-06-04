from typing import override
from tkinter import *
from pynput.keyboard import Key, Listener
from View.View import View
import threading
from Controller.IGameInteraction import IGameInteraction
from Model.Difficulty import Difficulty


class SudokuView(View):
    def __init__(self, game_interaction):
        self._grid = None
        self._cell_selected_ids = [[0 for _ in range(9)] for _ in range(9)]
        self._cell_highlighted_ids = [[0 for _ in range(9)] for _ in range(9)]
        self._cell_hitbox_ids = [[0 for _ in range(9)] for _ in range(9)]
        self._cell_value_ids = [[0 for _ in range(9)] for _ in range(9)]
        self._selected_cell = (-1, -1)
        self._marks_on = False

        # start a thread for listening for keyboard events
        listener_thread = threading.Thread(target=self._start_listener, daemon=True)
        listener_thread.start()

        super().__init__(game_interaction)

    @override
    def _create(self):
        # create root of the frame
        self._root = Tk()
        self._root.resizable(False, False)
        self._root.title("Sudoku 9x9")
        self._root.geometry('551x600')

        cell_size = 50

        # create sudoku grid as a canvas
        self._grid = Canvas(self._root, width=453, height=453)
        self._grid.place(x=49, y=30)

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

        self._root.mainloop()

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
        print("Listener thread started...")
        with Listener(on_press=self._cell_input) as listener:
            listener.join()

    def _cell_input(self, key):
        # if keys 1-9 are pressed either from keyboard or numpad, insert the respective value into the selected cell
        # if backspace is pressed, remove the value from the selected cell
        # ignore all other keys
        if self._selected_cell[0] != -1 and self._selected_cell[1] != -1:
            if key == Key.backspace:
                self._insert_number(0, self._selected_cell[0], self._selected_cell[1])
            try:
                if 97 <= key.vk <= 105:
                    self._insert_number(key.vk - 96, self._selected_cell[0], self._selected_cell[1])
                elif 49 <= key.vk <= 57:
                    self._insert_number(key.vk - 48, self._selected_cell[0], self._selected_cell[1])
                else:
                    pass
            except AttributeError:
                pass

    def _insert_number(self, value, x, y):
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

                self._cell_value_ids[y][x] = self._grid.create_text(
                    cell_x, cell_y,
                    text=str(value),
                    font=('Helvetica', 24),
                    fill='black'
                )
                # move the text below the hitbox, so that it's not covered by the text
                self._grid.tag_lower(self._cell_value_ids[y][x],
                                     self._cell_hitbox_ids[y][x])

            # remove the value from the cell if it's not empty, and the value is 0 (backspace pressed)
            if self._cell_value_ids[y][x] != 0 and value == 0:
                self._grid.delete(self._cell_value_ids[y][x])
                self._cell_value_ids[y][x] = 0
