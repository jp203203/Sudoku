from enum import Enum
from random import randint


class Difficulty(Enum):
    EASY = 35
    MEDIUM = 30
    HARD = 25


class Generator:
    def __init__(self, difficulty):
        if not isinstance(difficulty, Difficulty):
            raise TypeError("wrong difficulty value!")

        self.difficulty = difficulty
        print("difficulty value: ", difficulty.name, ", number of clues: ", difficulty.value, sep="")
        self.grid = None

    # generate grid using backtracking algorithm
    def generate_grid(self):
        self.grid = [[0] * 9 for i in range(9)]  # creating an empty grid (filled with zeroes)
        self.grid[randint(0, 8)][randint(0, 8)] = randint(1, 9)  # starting with a random element
        print("grid with one random cell filled:")
        self.print_grid()

        self.backtrack_fill(0, 0)
        print("fully filled grid:")
        self.print_grid()

    # implementation of backtracking algorithm for finding valid sudoku solutions
    def backtrack_fill(self, x_pos, y_pos):
        figure = randint(0, 8)  # first figure chosen randomly to make the puzzles less repetitive
        fig_limit = figure + 9
        valid_found = False

        # calculate next cell position
        next_x = (x_pos + 1) % 9
        next_y = y_pos + 1 if next_x == 0 else y_pos

        cell_empty = (self.grid[y_pos][x_pos] == 0)  # check if cell is empty

        while cell_empty and figure < fig_limit:  # if cell isn't empty, this loop can be skipped
            goto_next_figure = False
            self.grid[y_pos][x_pos] = (figure % 9) + 1

            # check if valid in subgrid
            for i in range((y_pos // 3) * 3, ((y_pos // 3) * 3) + 3):
                for j in range((x_pos // 3) * 3, ((x_pos // 3) * 3) + 3):
                    if not (i == y_pos and j == x_pos) and self.grid[i][j] == self.grid[y_pos][x_pos]:
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
                if x_pos != i and self.grid[y_pos][x_pos] == self.grid[y_pos][i]:
                    goto_next_figure = True
                    break

            # like previously, if invalid in row, go to next figure
            if goto_next_figure:
                figure += 1
                continue

            # check if valid in column
            for i in range(9):
                if y_pos != i and self.grid[y_pos][x_pos] == self.grid[i][x_pos]:
                    goto_next_figure = True
                    break

            # if still invalid, go to next figure
            if goto_next_figure:
                figure += 1
                continue

            #  if this cell is valid, check if the next cells are also valid
            #  if they're not - increment the figure on this one
            #  if this is the last cell, set the valid_found to true
            if not (x_pos == 8 and y_pos == 8):
                valid_found = self.backtrack_fill(next_x, next_y)

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
            valid_found = self.backtrack_fill(next_x, next_y)

        # "empty" the cell if none of the solutions are valid (and cell was empty)
        if not valid_found and cell_empty:
            self.grid[y_pos][x_pos] = 0

        return valid_found

    def print_grid(self):
        for i in range(9):
            for j in range(9):
                print(self.grid[i][j], end=" ")
            print()
        print()
