from reference_player.utils import guiFn
from reference_player.player_window import PlayerWindow
import sys
from PySide2 import QtWidgets

from reference_player import Logger
from reference_player import Config
Logger.set_level(Config.get("logging.level", default=10))
Logger.write_to_rotating_file(path="reference_player.log", level=40)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
    app.setPalette(guiFn.dark_pallete())

    main_window = PlayerWindow()
    main_window.show()
    app.exec_()
