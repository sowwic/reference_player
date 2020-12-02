from PySide2 import QtCore
from PySide2 import QtWidgets
from reference_player import Logger


class PlaybackSlider(QtWidgets.QSlider):
    def __init__(self, orientation=QtCore.Qt.Horizontal, handle_label="", parent=None) -> None:
        super().__init__(orientation, parent)
        self.handle_label = QtWidgets.QLabel(handle_label)
        # self.setTracking(True)
        self.create_connections()

    def update_label(self, value: int):
        # TODO: Not visible?
        height = QtWidgets.QStyle.sliderPositionFromValue(0, 100, value, self.height() - self.handle_label.height(), True)
        self.handle_label.move(self.width(), height)
        self.handle_label.setText(str(self.value()))

    def create_connections(self):
        self.valueChanged.connect(self.update_label)
