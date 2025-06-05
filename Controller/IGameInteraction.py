from abc import ABC, abstractmethod
from Model.Difficulty import Difficulty


class IGameInteraction(ABC):
    @abstractmethod
    def choose_difficulty(self, difficulty):
        pass

    @abstractmethod
    def pencil_mark(self, x, y, value):
        pass

    @abstractmethod
    def insert_cell(self, x, y, value):
        pass

    @abstractmethod
    def get_hint(self, x, y):
        pass
