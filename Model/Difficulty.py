from enum import Enum


class Difficulty(Enum):
    # difficulty enum defining cell count threshold and possible mistakes count
    EASY = 55
    MEDIUM = 45
    HARD = 35
    BIG = 150
