from PySide2 import QtWidgets


class QDMediaControls(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.slider = QtWidgets.QSlider()

    def create_layouts(self):
        pass

    def create_connections(self):
        pass
