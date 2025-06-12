from typing import override
from random import randint
from GameGenerator import GameGenerator
from RegGridSolver import RegGridSolver
from Model.Difficulty import Difficulty
from Model.RegSudokuGame import RegSudokuGame


class RegGameGenerator(GameGenerator):
    def __init__(self):
        super().__init__()

    # implementation of backtracking algorithm for finding valid sudoku solutions
    @override
    def _backtrack_fill(self, x, y):
        if y == 9 and x == 0:
            return True

        figure = randint(0, 8)  # first figure chosen randomly to make the puzzles less repetitive
        fig_limit = figure + 9
        valid_found = False

        # calculate next cell position
        next_x = (x + 1) % 9
        next_y = y + 1 if next_x == 0 and y < 8 else y

        cell_empty = (self._full_grid[y][x] == 0)  # check if cell is empty

        while cell_empty and figure < fig_limit:  # if cell isn't empty, this loop can be skipped
            goto_next_figure = False
            self._full_grid[y][x] = (figure % 9) + 1

            # check if valid in subgrid
            for i in range((y // 3) * 3, ((y // 3) * 3) + 3):
                for j in range((x // 3) * 3, ((x // 3) * 3) + 3):
                    if not (i == y and j == x) and self._full_grid[i][j] == self._full_grid[y][x]:
                        goto_next_figure = True
                    if goto_next_figure:  # break out of inner loop if figure is invalid at this point
                        break
                if goto_next_figure:  # same as above
                    break

            # if found invalid in subgrid, no point checking rows and columns - check the next figure
            if goto_next_figure:
                figure += 1
                continue

            # check if valid in row
            for i in range(9):
                if x != i and self._full_grid[y][x] == self._full_grid[y][i]:
                    goto_next_figure = True
                    break

            # like previously, if invalid in row, go to next figure
            if goto_next_figure:
                figure += 1
                continue

            # check if valid in column
            for i in range(9):
                if y != i and self._full_grid[y][x] == self._full_grid[i][x]:
                    goto_next_figure = True
                    break

            # if still invalid, go to next figure
            if goto_next_figure:
                figure += 1
                continue

            #  if this cell is valid, check if the next cells are also valid
            #  if they're not - increment the figure on this one
            #  if this is the last cell, set the valid_found to true
            if not (x == 8 and y == 8):
                valid_found = self._backtrack_fill(next_x, next_y)

                if not valid_found:
                    figure += 1
                    continue
            else:
                valid_found = True

            # break out of loop if valid solution is found
            if valid_found:
                break

        # if cell wasn't empty, check the next cells
        if not cell_empty:
            valid_found = self._backtrack_fill(next_x, next_y)

        # "empty" the cell if none of the solutions are valid (and cell was empty)
        if not valid_found and cell_empty:
            self._full_grid[y][x] = 0

        return valid_found

    # generate full grid using backtracking algorithm
    @override
    def _generate_full_grid(self):
        self._full_grid = [[0] * 9 for _ in range(9)]  # creating an empty grid (filled with zeroes)
        self._full_grid[randint(0, 8)][randint(0, 8)] = randint(1, 9)  # starting with a random element

        self._backtrack_fill(0, 0)

    # creates solvable grid  based on the full grid
    @override
    def _generate_solvable_grid(self, difficulty):
        # first, generate full grid
        self._generate_full_grid()
        self._solvable_grid = [row[:] for row in self._full_grid]  # copy the full grid into solvable grid

        filled_by_row = [9] * 9
        filled_by_col = [9] * 9
        filled_cells = 81

        self._solver = RegGridSolver()  # make new instance of GridSolver

        # remove cells as long as the grid is solvable for chosen difficulty
        solvable = True
        while solvable:
            # find a random cell to empty
            row = randint(0, 8)
            col = randint(0, 8)

            # check requirements:
            # cell can't be empty, row and column can't have less than 2 cells filled if difficulty is not hard
            while (self._solvable_grid[col][row] == 0 or
                   (difficulty != Difficulty.HARD and
                    (filled_by_col[col] == 2 or filled_by_row[row] == 2))):
                # if requirements not met, find new cell
                row = randint(0, 8)
                col = randint(0, 8)

            prev_value = self._full_grid[col][row]  # read the cell value in case it needs to be put back into the cell
            self._solvable_grid[col][row] = 0  # empty the cell
            # copy the solvable grid to pass to the solver
            self._solvable_grid_copy = [row[:] for row in self._solvable_grid]
            filled_cells -= 1
            filled_by_row[row] -= 1
            filled_by_col[col] -= 1

            solvable = self._solver.try_solving(self._solvable_grid_copy, filled_cells, difficulty)
            if not solvable:
                # write the value back to the cell if grid isn't solvable anymore
                self._solvable_grid[col][row] = prev_value
                filled_cells += 1

        # return filled cells left after emptying the grid, to check whether the threshold is met
        return filled_cells

    # creates a new sudoku game based on the difficulty
    @override
    def generate_game(self, difficulty):
        filled_cells = 0

        eligible = False
        while not eligible:
            eligible = True
            filled_cells = self._generate_solvable_grid(difficulty)
            if filled_cells > difficulty.value:
                eligible = False

        return RegSudokuGame(self._full_grid, self._solvable_grid, filled_cells, difficulty)
