from abc import ABC, abstractmethod


class IGameViewUpdate(ABC):
    @abstractmethod
    def update_cell(self, x, y, value, correct):
        pass

    @abstractmethod
    def update_mistakes(self, mistakes_left):
        pass

    @abstractmethod
    def finish_game(self, won):
        pass
