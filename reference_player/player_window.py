import cv2
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

from reference_player import __version__
from reference_player import Logger
from reference_player import Config
from reference_player import MainWindowVars
from reference_player.core.client import MayaClient


class PlayerWindow(QtWidgets.QMainWindow):
    DEFAULT_SIZE = (600, 400)
    MINIMUM_SIZE = (400, 300)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Window properties
        self.setWindowTitle("Reference player")

        # Initialize UI
        self.create_actions()
        self.create_menubar()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        # Load previous position and size
        self.resize(QtCore.QSize(*Config.get(MainWindowVars.size, default=self.DEFAULT_SIZE)))
        self.move(QtCore.QPoint(*Config.get(MainWindowVars.position, default=(0, 0))))

    def create_actions(self):
        pass

    def create_menubar(self):
        self.main_menubar: QtWidgets.QMenuBar = self.menuBar()
        self.file_menu = self.main_menubar.addMenu("&File")
        self.edit_menu = self.main_menubar.addMenu("Edit")
        self.tools_menu = self.main_menubar.addMenu("Tools")
        self.help_menu = self.main_menubar.addMenu("Help")

    def create_widgets(self):
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget.setLayout(self.main_layout)

    def create_connections(self):
        pass

    def closeEvent(self, event):
        Config.set(MainWindowVars.position, [self.pos().x(), self.pos().y()])
        Config.set(MainWindowVars.size, [self.width(), self.height()])
        Logger.debug("Saved main window size and position.")
        super().closeEvent(event)
