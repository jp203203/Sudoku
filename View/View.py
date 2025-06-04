from abc import ABC, abstractmethod


class View(ABC):
    def __init__(self, game_interaction):
        self._game_interaction = game_interaction
        self._root = None
        self._create()

    @abstractmethod
    def _create(self):
        pass
