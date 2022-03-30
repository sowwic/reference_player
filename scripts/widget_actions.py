from PySide2 import QtCore
from PySide2 import QtWidgets


class QLabeledSliderWidget(QtWidgets.QWidget):
    def __init__(self, label: str, values_range: tuple[int, int], parent: QtCore.QObject = None):
        super().__init__(parent=parent)
        self.slider = QtWidgets.QSlider()
        self.slider.setRange(*values_range)
        self.slider.setOrientation(QtCore.Qt.Horizontal)

        self.main_layout = QtWidgets.QFormLayout()
        self.main_layout.addRow(label, self.slider)
        self.setLayout(self.main_layout)
