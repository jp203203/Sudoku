from typing import override
from tkinter import *
from tkinter.font import Font
from View.View import View
from View.SudokuView import SudokuView
from Controller.IGameInteraction import IGameInteraction
from Model.Difficulty import Difficulty


class BigSudokuView(SudokuView):
    val_sym = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
               10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G'}

    def __init__(self, game_interaction):
        super().__init__(game_interaction, board_size=16)

    @override
    def _create(self):
        # create root of the frame
        self._root = Tk()
        # add key binding
        self._root.bind("<Key>", self._on_key_press)
        # handle window close event
        self._root.protocol("WM_DELETE_WINDOW", self._game_interaction.new_game)

        self._root.resizable(False, False)
        self._root.title("Sudoku 16x16")
        self._root.geometry('773x822')
        self._root.rowconfigure((0, 1), weight=1)
        self._root.columnconfigure((0, 1, 2), weight=1)

        cell_size = 42

        # create sudoku grid as a canvas
        self._grid = Canvas(self._root, width=675, height=675)
        self._grid.grid(row=0, column=0, columnspan=3)

        # create colored squares for selected and highlighted cells, and hide them
        # additionally create click event listeners as transparent hitboxes
        for row in range(16):
            for cell in range(16):
                x0 = cell_size * cell + 4
                y0 = cell_size * row + 4
                x1 = x0 + 41
                y1 = y0 + 41

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
                for mark_row in range(4):
                    for mark_col in range(4):
                        mark_x = x0 + 6 + 10 * mark_col
                        mark_y = y0 + 6 + 10 * mark_row
                        self._cell_mark_ids[row][cell][mark_idx] = self._grid.create_text(
                            mark_x, mark_y,
                            text=str(BigSudokuView.val_sym[mark_idx + 1]),
                            font=('Helvetica', 8),
                            fill='#4a4a4a'
                        )
                        self._grid.itemconfig(self._cell_mark_ids[row][cell][mark_idx], state='hidden')
                        mark_idx += 1

                # create hitboxes
                self._cell_hitbox_ids[row][cell] = self._grid.create_rectangle(x0, y0, x1, y1,
                                                                               width=0, fill='', outline='')
                self._grid.tag_bind(self._cell_hitbox_ids[row][cell], '<Button-1>',
                                    lambda e, x=cell, y=row: self._select_cells(x, y))

        for i in range(17):
            # add vertical and horizontal lines
            line_width = 3 if i % 4 == 0 else 1
            self._grid.create_line(i * cell_size + 3, 0, i * cell_size + 3, 676, width=line_width)
            self._grid.create_line(0, i * cell_size + 3, 676, i * cell_size + 3, width=line_width)

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

    # highlight selected cell and all cells in the same row, column and sub_grid
    @override
    def _select_cells(self, x, y):
        # hide previous highlights first
        for i in range(16):
            for j in range(16):
                self._grid.itemconfig(self._cell_highlighted_ids[i][j], state='hidden')
                self._grid.itemconfig(self._cell_selected_ids[i][j], state='hidden')

        # highlight selected cell
        self._grid.itemconfig(self._cell_selected_ids[y][x], state='normal')

        # highlight cells in the same row
        for i in range(16):
            if i != x:
                self._grid.itemconfig(self._cell_highlighted_ids[y][i], state='normal')

        # highlight cells in the same column
        for i in range(16):
            if i != y:
                self._grid.itemconfig(self._cell_highlighted_ids[i][x], state='normal')

        # highlight cells in the same sub-grid
        first_x = (x // 4) * 4
        first_y = (y // 4) * 4

        for i in range(first_y, first_y + 4):
            for j in range(first_x, first_x + 4):
                self._grid.itemconfig(self._cell_highlighted_ids[i][j], state='normal')

        self._selected_cell = (x, y)

    @override
    def _write_number(self, value, x, y, correct):
        # determine the position of the value to be inserted
        cell_size = 42
        cell_x = cell_size * x + 25
        cell_y = cell_size * y + 25

        if self._grid is not None:
            # fill the cell if the value is not 0 (key 1-9 or A-G pressed)
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
                    text=BigSudokuView.val_sym[value],
                    font=('Helvetica', 23),
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
            for i in range(16):
                self._grid.itemconfig(self._cell_mark_ids[y][x][i], state='hidden')

            # update the marks if inserted value is correct
            if correct:
                self._update_marks(x, y, value)

    @override
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
            elif event.char in '123456789':
                value = int(event.char)
            elif event.char.upper() in 'ABCDEFG':
                value = ord(event.char.upper()) - ord('A') + 10
            elif event.char.upper() == 'W':
                self._game_interaction.win()
            else:
                return

            action(x, y, value)

    @override
    def _update_marks(self, x, y, value):
        # remove the marks from correct spot
        for i in range(16):
            self._grid.delete(self._cell_mark_ids[y][x][i])

        # hide pencil marks for the same row
        for col_idx in range(16):
            if col_idx != x:
                self._grid.itemconfig(self._cell_mark_ids[y][col_idx][value-1], state='hidden')

        # hide pencil marks for the same column
        for row_idx in range(16):
            if row_idx != y:
                self._grid.itemconfig(self._cell_mark_ids[row_idx][x][value-1], state='hidden')

        first_x = (x // 4) * 4
        first_y = (y // 4) * 4

        for row_idx in range(first_y, first_y + 4):
            for col_idx in range(first_x, first_x + 4):
                if not (row_idx == y and col_idx == x):
                    self._grid.itemconfig(self._cell_mark_ids[row_idx][col_idx][value-1], state='hidden')
