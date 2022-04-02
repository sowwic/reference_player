from PySide2 import (QtCore,
                     QtWidgets)


class QDTimeSlider(QtWidgets.QSlider):
    def __init__(self, parent=None):
        super().__init__(QtCore.Qt.Horizontal, parent=parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.setTickPosition(QtWidgets.QSlider.TicksBothSides)

    def create_layouts(self):
        pass

    def create_connections(self):
        pass

    def set_time_range(self, time_range: tuple[int, int]):
        self.setRange(*time_range)
        self.setTickInterval((self.maximum() - self.minimum()) / 10)
