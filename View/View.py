from abc import ABC, abstractmethod


class View(ABC):
    def __init__(self, game_interaction):
        self._game_interaction = game_interaction
        self._root = None
        self._create()
        self._center_frame()

    @abstractmethod
    def _create(self):
        pass

    def start(self):
        self._root.mainloop()

    def get_root(self):
        return self._root

    def _center_frame(self):
        self._root.update_idletasks()
        width = self._root.winfo_width()
        height = self._root.winfo_height()
        screen_width = self._root.winfo_screenwidth()
        screen_height = self._root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self._root.geometry(f"{width}x{height}+{x}+{y}")

    def _close(self):
        self._root.destroy()
        self._game_interaction.terminate()
