import cv2
import pathlib
from functools import partial
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

from reference_player import Logger
from reference_player import Config
from reference_player.core.client import MayaClient
from reference_player.core.reference import Reference
from reference_player.utils import guiFn
from reference_player.widgets.playback_widget import QDPlaybackWidget
from reference_player.widgets import menus


class PlayerWindow(QtWidgets.QMainWindow):
    MINIMUM_SIZE = (400, 300)

    @property
    def config(self) -> Config:
        return QtWidgets.QApplication.instance().config

    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent)

        # Window properties
        self.setWindowTitle("Reference player")
        self.setWindowIcon(guiFn.get_icon("player_icon.ico"))
        self.setMinimumSize(*self.MINIMUM_SIZE)

        # Initialize UI
        self.create_actions()
        self.create_menubar()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.apply_config_values()

        # Maya client
        self.maya_client = MayaClient(self.config.maya_port)
        if self.config.maya_autoconnect:
            self.maya_client.connect()

    def create_actions(self):
        """Create and configure QActions"""
        pass

    def create_menubar(self):
        """Create and populate menubar"""
        self.main_menubar: QtWidgets.QMenuBar = self.menuBar()
        self.main_menubar.setNativeMenuBar(False)
        self.pin_window_btn = QtWidgets.QPushButton()
        self.pin_window_btn.setToolTip("Toggle always on top")
        self.pin_window_btn.setIcon(guiFn.get_icon("pinned.png"))
        self.pin_window_btn.setFlat(True)
        self.pin_window_btn.setCheckable(True)
        self.main_menubar.setCornerWidget(self.pin_window_btn, QtCore.Qt.TopRightCorner)

        self.file_menu = menus.FileMenu(self)
        self.edit_menu = menus.EditMenu(self)
        self.tools_menu = menus.ToolsMenu(self)
        self.help_menu = menus.HelpMenu(self)

        self.main_menubar.addMenu(self.file_menu)
        self.main_menubar.addMenu(self.edit_menu)
        self.main_menubar.addMenu(self.tools_menu)
        self.main_menubar.addMenu(self.help_menu)

    def create_widgets(self):
        """Create and configure widgets"""
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)

        self.video_tabs = QtWidgets.QTabWidget()
        self.video_tabs.setTabsClosable(True)

    def create_layouts(self):
        """Create and populate layouts"""
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.video_tabs)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget.setLayout(self.main_layout)

    def create_connections(self):
        """Create signal to slot connections"""
        # Actions
        self.pin_window_btn.toggled.connect(self.toggle_always_on_top)
        self.file_menu.file_new_action.triggered.connect(self.new_reference)
        self.file_menu.file_open_action.triggered.connect(self.open_reference_file)
        self.tools_menu.maya_port_action.triggered.connect(self.set_maya_port)
        self.help_menu.debug_logging_action.toggled.connect(self.set_debug_logging)
        self.help_menu.reset_config_action.triggered.connect(self.reset_application_config)

        # Tabs
        self.video_tabs.tabCloseRequested.connect(lambda index: self.handle_tab_close(index))

    def closeEvent(self, event: QtCore.QEvent):
        """
        Override close event to:

        - Save config values
        """
        self.save_config_values()
        super().closeEvent(event)

    def save_config_values(self):
        """Set values for config."""
        self.config.window_position = (self.pos().x(), self.pos().y())
        self.config.window_size = (self.width(), self.height())
        self.config.window_always_on_top = self.pin_window_btn.isChecked()
        self.config.maya_autoconnect = self.tools_menu.maya_auto_connect_action.isChecked()

    def apply_config_values(self):
        """Apply values from application config."""
        self.resize(QtCore.QSize(*self.config.window_size))
        if not self.config.window_position:
            center_position: QtCore.QPoint = self.pos(
            ) + QtWidgets.QApplication.primaryScreen().geometry().center() - self.geometry().center()
            self.config.window_position = (center_position.x(), center_position.y())
        self.move(QtCore.QPoint(*self.config.window_position))

        self.toggle_always_on_top(self.config.window_always_on_top)
        Logger.set_level(self.config.logging_level)

    def reset_application_config(self):
        """Reset application config and apply changes."""
        QtWidgets.QApplication.instance().reset_config()
        self.apply_config_values()

    def new_reference(self):
        new_ref = Reference(dict())
        return self.add_new_reference_tab(new_ref)

    def open_reference_file(self):
        """Opens file dialog for choosing a video file.

        If video file already open in one of the tabs - sets it active.
        """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open reference file", None)
        if not file_path:
            return

        file_path = pathlib.Path(file_path)
        if not file_path.is_file():
            Logger.error("Not a file: {0}".format(file_path))
            return

        reference = Reference.from_file(file_path)
        new_playback = QDPlaybackWidget(reference)
        self.video_tabs.addTab(new_playback, new_playback.reference.name)

    def add_new_reference_tab(self, reference: Reference):
        new_playback = QDPlaybackWidget(reference)
        self.video_tabs.addTab(new_playback, new_playback.reference.name)
        return new_playback

    def handle_tab_close(self, index: int):
        """Handles operation of closing a tab and deleting a playback widget.

        Args:
            index (int): index of tab to close
        """
        widget: QDPlaybackWidget = self.video_tabs.widget(index)
        self.video_tabs.removeTab(index)
        widget.media_player.pause()
        widget.deleteLater()

    def toggle_always_on_top(self, state: bool):
        """Sets window always on top flag and reshows the window.

        Args:
            state (bool): _description_
        """
        if state:
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        self.pin_window_btn.setChecked(state)
        self.show()

    def set_maya_port(self):
        """Show dialog for setting Maya TCP connection port."""
        value, result = QtWidgets.QInputDialog.getInt(
            self, "Maya port", "Port number:", self.config.maya_port, minValue=1024, maxValue=65535)
        if result:
            self.config.maya_port = value

    def set_debug_logging(self, state):
        debug_state = {True: 10,
                       False: 20}
        Logger.set_level(debug_state[state])
        self.config.logging_level = debug_state[state]
