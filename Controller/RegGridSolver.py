from typing import override
from Model.Difficulty import Difficulty
from GridSolver import GridSolver


class RegGridSolver(GridSolver):
    def __init__(self):
        super().__init__()

    # create pencil marks for the sudoku grid, symbolizing candidates for each cell
    @override
    def _create_pencil_marks(self):
        # create full pencil marks
        self.__pencil_marks = [[[True for i in range(9)] for i in range(9)] for i in range(9)]

        for i in range(9):
            for j in range(9):
                # remove all marks from cells which are already filled out
                if self._grid[i][j] != 0:
                    self.__pencil_marks[i][j] = [False for mark in range(9)]
                # otherwise, remove spaces based on cells filled out in the same row, column and subgrid
                else:
                    for column_idx in range(9):  # check the row first
                        if j == column_idx:
                            continue  # skip the column index of the current cell

                        cell_val = self._grid[i][column_idx]
                        if cell_val != 0:
                            self.__pencil_marks[i][j][cell_val - 1] = False

                    for row_idx in range(9):  # then, check the column
                        if i == row_idx:
                            continue  # skip the row index of the current cell

                        cell_val = self._grid[row_idx][j]
                        if cell_val != 0:
                            self.__pencil_marks[i][j][cell_val - 1] = False

                    sub_first_x = 3 * (j // 3)
                    sub_first_y = 3 * (i // 3)
                    for column_idx in range(3):  # at last, check the subgrid
                        for row_idx in range(3):
                            # skip the current cell
                            if j == (column_idx + sub_first_x) and i == (row_idx + sub_first_y):
                                continue

                            cell_val = self._grid[row_idx + sub_first_y][column_idx + sub_first_x]
                            if cell_val != 0:
                                self.__pencil_marks[i][j][cell_val - 1] = False

    # insert the value into the cell and update pencil marks
    @override
    def _insert_cell(self, y_pos, x_pos, value):
        self._grid[y_pos][x_pos] = value + 1  # insert the value into the cell

        # update the pencil marks
        self.__pencil_marks[y_pos][x_pos] = [False for mark in range(9)]

        for column_idx in range(9):
            if column_idx == x_pos:
                continue
            self.__pencil_marks[y_pos][column_idx][value] = False

        for row_idx in range(9):
            if row_idx == y_pos:
                continue
            self.__pencil_marks[row_idx][x_pos][value] = False

        sub_first_x = 3 * (x_pos // 3)
        sub_first_y = 3 * (y_pos // 3)
        for column_idx in range(3):
            for row_idx in range(3):
                if x_pos == (column_idx + sub_first_x) and y_pos == (row_idx + sub_first_y):
                    continue
                self.__pencil_marks[row_idx + sub_first_y][column_idx + sub_first_x][value] = False

    # try filling out a space using the "hidden singles" technique
    @override
    def _try_hidden_singles(self):
        updated = False

        # first, check rows
        for i in range(9):
            for value in range(9):
                last_valid_cell = -1
                valid_cell_count = 0
                for j in range(9):
                    if self.__pencil_marks[i][j][value]:
                        last_valid_cell = j
                        valid_cell_count += 1

                if valid_cell_count == 1:
                    self._insert_cell(i, last_valid_cell, value)
                    updated = True
                    self._filled_cells += 1

        # check columns
        for j in range(9):
            for value in range(9):
                last_valid_cell = -1
                valid_cell_count = 0
                for i in range(9):
                    if self.__pencil_marks[i][j][value]:
                        last_valid_cell = i
                        valid_cell_count += 1

                if valid_cell_count == 1:
                    self._insert_cell(last_valid_cell, j, value)
                    updated = True
                    self._filled_cells += 1

        # check sub-grids
        for i in range(3):
            for j in range(3):
                sub_first_row = 3 * i
                sub_first_col = 3 * j

                for value in range(9):
                    last_valid_cell = [-1, -1]
                    valid_cell_count = 0

                    for y in range(sub_first_row, sub_first_row + 3):
                        for x in range(sub_first_col, sub_first_col + 3):
                            if self.__pencil_marks[y][x][value]:
                                last_valid_cell = [y, x]
                                valid_cell_count += 1

                    if valid_cell_count == 1:
                        self._insert_cell(last_valid_cell[0], last_valid_cell[1], value)
                        updated = True
                        self._filled_cells += 1

        return updated

    # try filling out a space using the "naked singles" technique
    @override
    def _try_naked_singles(self):
        updated = False

        for i in range(9):
            for j in range(9):
                # check each cell to see if there is only one possible value for it
                if self.__pencil_marks[i][j].count(True) == 1:
                    # find the value and insert it into the cell
                    value = self.__pencil_marks[i][j].index(True)
                    self._insert_cell(i, j, value)
                    updated = True
                    self._filled_cells += 1

        return updated

    # try eliminating candidates (marks) from cells using the "hidden pairs" technique
    @override
    def _try_hidden_pairs(self):
        updated = False

        # start with rows
        for i in range(9):
            for val1 in range(9):
                for val2 in range(val1 + 1, 9):
                    val1_cells = []
                    val2_cells = []

                    for j in range(9):
                        if self.__pencil_marks[i][j][val1]:
                            val1_cells.append(j)
                        if self.__pencil_marks[i][j][val2]:
                            val2_cells.append(j)

                    # check if both values appear in only 2 cells
                    if len(val1_cells) == 2 and val1_cells == val2_cells:
                        changes_made = False
                        # update pencil marks in the whole row
                        for col_idx in range(9):
                            if col_idx in val1_cells:
                                # for cells with a hidden pair, remove all values but the ones from the pair
                                for pm_val in range(9):
                                    if pm_val != val1 and pm_val != val2 and self.__pencil_marks[i][col_idx][pm_val]:
                                        self.__pencil_marks[i][col_idx][pm_val] = False
                                        changes_made = True
                            else:
                                # for cells without the pair, remove only the values from the pair
                                if self.__pencil_marks[i][col_idx][val1]:
                                    self.__pencil_marks[i][col_idx][val1] = False
                                    changes_made = True
                                if self.__pencil_marks[i][col_idx][val2]:
                                    self.__pencil_marks[i][col_idx][val2] = False
                                    changes_made = True

                        if changes_made:
                            updated = True

        # check columns next
        for j in range(9):
            for val1 in range(9):
                for val2 in range(val1 + 1, 9):
                    val1_cells = []
                    val2_cells = []

                    for i in range(9):
                        if self.__pencil_marks[i][j][val1]:
                            val1_cells.append(i)
                        if self.__pencil_marks[i][j][val2]:
                            val2_cells.append(i)

                    # check if both values appear in only 2 cells
                    if len(val1_cells) == 2 and val1_cells == val2_cells:
                        changes_made = False
                        # update pencil marks in the whole column
                        for row_idx in range(9):
                            if row_idx in val1_cells:
                                # for cells with a hidden pair, remove all values but the ones from the pair
                                for pm_val in range(9):
                                    if pm_val != val1 and pm_val != val2 and self.__pencil_marks[row_idx][j][pm_val]:
                                        self.__pencil_marks[row_idx][j][pm_val] = False
                                        changes_made = True
                            else:
                                # for cells without the pair, remove only the values from the pair
                                if self.__pencil_marks[row_idx][j][val1]:
                                    self.__pencil_marks[row_idx][j][val1] = False
                                    changes_made = True
                                if self.__pencil_marks[row_idx][j][val2]:
                                    self.__pencil_marks[row_idx][j][val2] = False
                                    changes_made = True

                        if changes_made:
                            updated = True

        # last, check sub-grids
        for i in range(3):
            for j in range(3):
                sub_first_row = 3 * i
                sub_first_col = 3 * j

                for val1 in range(9):
                    for val2 in range(val1 + 1, 9):
                        val1_cells = []
                        val2_cells = []

                        for y in range(sub_first_row, sub_first_row + 3):
                            for x in range(sub_first_col, sub_first_col + 3):
                                if self.__pencil_marks[y][x][val1]:
                                    val1_cells.append([y, x])
                                if self.__pencil_marks[y][x][val2]:
                                    val2_cells.append([y, x])

                        # check if both values appear in only 2 cells
                        if len(val1_cells) == 2 and val1_cells == val2_cells:
                            changes_made = False
                            # update pencil marks in the whole sub-grid
                            for row_idx in range(sub_first_row, sub_first_row + 3):
                                for col_idx in range(sub_first_col, sub_first_col + 3):
                                    if [row_idx, col_idx] in val1_cells:
                                        # for cells with a hidden pair, remove all values but the ones from the pair
                                        for pm_val in range(9):
                                            if pm_val != val1 and pm_val != val2 and \
                                                    self.__pencil_marks[row_idx][col_idx][pm_val]:
                                                self.__pencil_marks[row_idx][col_idx][pm_val] = False
                                                changes_made = True
                                    else:
                                        # for cells without the pair, remove only the values from the pair
                                        if self.__pencil_marks[row_idx][col_idx][val1]:
                                            self.__pencil_marks[row_idx][col_idx][val1] = False
                                            changes_made = True
                                        if self.__pencil_marks[row_idx][col_idx][val2]:
                                            self.__pencil_marks[row_idx][col_idx][val2] = False
                                            changes_made = True

                            if changes_made:
                                updated = True

        return updated

    # try solving the grid using different methods (based on difficulty)
    @override
    def try_solving(self, grid, filled_cells, difficulty):
        self._grid = grid

        if not isinstance(difficulty, Difficulty):
            raise ValueError("Incorrect difficulty value!")
        self._filled_cells = filled_cells

        self._create_pencil_marks()  # create pencil marks first

        updated = True
        while updated:
            updated = False

            # for all difficulties, try the "hidden singles" technique
            updated = self._try_hidden_singles()

            # if all cells are filled, break out of the loop
            if self._filled_cells == 81:
                break

            if difficulty == Difficulty.EASY:
                continue

            # for medium and hard difficulties, try the "naked singles" technique
            updated = self._try_naked_singles()

            if filled_cells == 81:
                break

            if difficulty == Difficulty.MEDIUM:
                continue

            # for hard difficulty, try the "hidden pairs" technique
            updated = self._try_hidden_pairs()

            # no check of filled cells after using hidden pairs, because no cells were filled

        # return True if grid was solved, and False otherwise
        if self._filled_cells == 81:
            return True
        else:
            return False
