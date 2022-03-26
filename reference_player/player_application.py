from PySide2 import QtWidgets

from reference_player.utils import guiFn
from reference_player.player_window import PlayerWindow
from reference_player import Logger
from reference_player import Config


class QReferencePlayerApplication(QtWidgets.QApplication):
    def __init__(self, argv: list[str] = None):
        argv = argv if argv else []
        super().__init__(argv)
        self.config = Config.load()
        Logger.set_level(self.config.logging_level)
        Logger.write_to_rotating_file(path="reference_player.log", level=40)

        self.setStyle(QtWidgets.QStyleFactory.create("fusion"))
        self.setPalette(guiFn.dark_pallete())

        main_window = PlayerWindow()
        main_window.show()

    def reset_config(self):
        """Reset application config."""
        self.config = self.config.reset()
