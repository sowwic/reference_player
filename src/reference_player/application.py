import pathlib
from PySide6 import QtWidgets
from PySide6 import QtQml


APPLICATION_QML_SOURCE = (
    pathlib.Path(__file__).absolute().resolve().parent / "qml" / "application.qml"
)


class ReferencePlayerApplication(QtWidgets.QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.engine = QtQml.QQmlApplicationEngine()
        self.engine.quit.connect(self.quit)
        self.engine.load(APPLICATION_QML_SOURCE)
