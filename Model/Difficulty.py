from enum import Enum


class Difficulty(Enum):
    # difficulty enum defining cell count threshold and possible mistakes count
    EASY = (55, 1)
    MEDIUM = (45, 2)
    HARD = (35, 3)
    BIG = (257, 4)
