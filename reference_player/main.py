import sys
from PySide2 import QtWidgets

from reference_player import Logger
from reference_player import Config
from reference_player.player_window import PlayerWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = PlayerWindow()
    main_window.show()
    app.exec_()
