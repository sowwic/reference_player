import pathlib
from PySide6 import QtWidgets
from PySide6 import QtQml

from reference_player.version import __version__


APPLICATION_QML_SOURCE = (
    pathlib.Path(__file__).absolute().resolve().parent / "qml" / "Application.qml"
)


class ReferencePlayerApplication(QtWidgets.QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationVersion(__version__)
        self.setApplicationName("reference-player")
        self.setApplicationDisplayName(f"Reference Player v{__version__}")

        self.engine = QtQml.QQmlApplicationEngine()
        self.engine.quit.connect(self.quit)
        self.engine.load(APPLICATION_QML_SOURCE)
