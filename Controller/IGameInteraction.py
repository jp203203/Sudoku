from abc import ABC, abstractmethod
from Model.Difficulty import Difficulty


class IGameInteraction(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def choose_difficulty(self, difficulty):
        pass

    @abstractmethod
    def pencil_mark(self, x, y, value):
        pass

    @abstractmethod
    def fill_cell(self, x, y, value):
        pass
