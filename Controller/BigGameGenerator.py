from typing import override
from random import randint
from GameGenerator import GameGenerator
from BigGridSolver import BigGridSolver
from Model.Difficulty import Difficulty
from Model.BigSudokuGame import BigSudokuGame


class BigGameGenerator(GameGenerator):
    def __init__(self):
        super().__init__()

    # implementation of backtracking algorithm for finding valid sudoku solutions
    @override
    def _backtrack_fill(self, x, y):
        if y >= 15 and x >= 15:
            return True

        figure = randint(0, 15)  # first figure chosen randomly to make the puzzles less repetitive
        fig_limit = figure + 16
        valid_found = False

        # calculate next cell position
        next_x = (x + 1) % 16
        next_y = y + 1 if next_x == 0 and y < 15 else y

        cell_empty = (self._full_grid[y][x] == 0)  # check if cell is empty

        while cell_empty and figure < fig_limit:  # if cell isn't empty, this loop can be skipped
            goto_next_figure = False
            self._full_grid[y][x] = (figure % 16) + 1

            # check if valid in subgrid
            for i in range((y // 4) * 4, ((y // 4) * 4) + 4):
                for j in range((x // 4) * 4, ((x // 4) * 4) + 4):
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
            for i in range(16):
                if x != i and self._full_grid[y][x] == self._full_grid[y][i]:
                    goto_next_figure = True
                    break

            # like previously, if invalid in row, go to next figure
            if goto_next_figure:
                figure += 1
                continue

            # check if valid in column
            for i in range(16):
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
            if not (x == 15 and y == 15):
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
        self._full_grid = [[0] * 16 for _ in range(16)]  # creating an empty grid (filled with zeroes)
        self._full_grid[randint(0, 15)][randint(0, 15)] = randint(1, 16)  # starting with a random element

        self._backtrack_fill(0, 0)

    # creates solvable grid  based on the full grid
    @override
    def _generate_solvable_grid(self, difficulty=None):
        # first, generate full grid
        self._generate_full_grid()
        self._solvable_grid = [row[:] for row in self._full_grid]  # copy the full grid into solvable grid

        filled_by_row = [16] * 16
        filled_by_col = [16] * 16
        filled_cells = 256

        self._solver = BigGridSolver()  # make new instance of GridSolver

        # remove cells as long as the grid is solvable for chosen difficulty
        solvable = True
        while solvable:
            # find a random cell to empty
            row = randint(0, 15)
            col = randint(0, 15)

            # find new cell as long as the chosen one is already empty
            while self._solvable_grid[col][row] == 0:
                row = randint(0, 15)
                col = randint(0, 15)

            prev_value = self._full_grid[col][row]  # read the cell value in case it needs to be put back into the cell
            self._solvable_grid[col][row] = 0  # empty the cell
            # copy the solvable grid to pass to the solver
            self._solvable_grid_copy = [row[:] for row in self._solvable_grid]
            filled_cells -= 1
            filled_by_row[row] -= 1
            filled_by_col[col] -= 1

            solvable = self._solver.try_solving(self._solvable_grid_copy, filled_cells)
            if not solvable:
                # write the value back to the cell if grid isn't solvable anymore
                self._solvable_grid[col][row] = prev_value

        # return filled cells left after emptying the grid, to check whether the threshold is met
        return filled_cells

    # creates a new big sudoku game
    @override
    def generate_game(self, difficulty):
        if not isinstance(difficulty, Difficulty):
            raise ValueError("difficulty is not an instance of Difficulty enum")

        eligible = False
        while not eligible:
            eligible = True
            filled_cells = self._generate_solvable_grid(difficulty)
            if filled_cells > difficulty.value:
                eligible = False

        return BigSudokuGame(self._full_grid, self._solvable_grid)
