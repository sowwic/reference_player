from PySide2 import QtWidgets
from PySide2 import QtMultimediaWidgets
from PySide2 import QtMultimedia

from reference_player import Logger


class PlaybackWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
