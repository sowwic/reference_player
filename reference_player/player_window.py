import cv2
import pathlib
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

from reference_player import __version__
from reference_player import Logger
from reference_player import Config
from reference_player import MainWindowVars
from reference_player.core.client import MayaClient
from reference_player.core import rc_icons
from reference_player.widgets.playback_widget import PlaybackWidget


class PlayerWindow(QtWidgets.QMainWindow):
    DEFAULT_SIZE = (600, 400)
    MINIMUM_SIZE = (400, 300)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Window properties
        self.setWindowTitle("Reference player")
        self.setWindowIcon(QtGui.QIcon(":/images/player_icon.ico"))

        # Initialize UI
        self.create_actions()
        self.create_menubar()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        # Load previous position and size
        self.toggle_always_on_top(Config.get(MainWindowVars.always_on_top, default=False), update=False)
        self.resize(QtCore.QSize(*Config.get(MainWindowVars.size, default=self.DEFAULT_SIZE)))
        self.move(QtCore.QPoint(*Config.get(MainWindowVars.position, default=(0, 0))))

    def create_actions(self):
        self.file_open_action = QtWidgets.QAction(QtGui.QIcon("open.png"), "&Open", self)
        self.file_open_action.setShortcut("Ctrl+O")
        self.file_open_action.setStatusTip("Open video file")

    def create_menubar(self):
        self.main_menubar: QtWidgets.QMenuBar = self.menuBar()
        self.pin_window_btn = QtWidgets.QPushButton()
        self.pin_window_btn.setIcon(QtGui.QIcon(":/images/pinned.png"))
        self.pin_window_btn.setFlat(True)
        self.pin_window_btn.setCheckable(True)
        self.main_menubar.setCornerWidget(self.pin_window_btn, QtCore.Qt.TopRightCorner)
        self.file_menu: QtWidgets.QMenu = self.main_menubar.addMenu("&File")
        self.file_menu.addAction(self.file_open_action)

        self.edit_menu: QtWidgets.QMenu = self.main_menubar.addMenu("Edit")
        self.tools_menu: QtWidgets.QMenu = self.main_menubar.addMenu("Tools")
        self.help_menu: QtWidgets.QMenu = self.main_menubar.addMenu("Help")

    def create_widgets(self):
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)

        self.video_tabs = QtWidgets.QTabWidget()
        self.video_tabs.setTabsClosable(True)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.video_tabs)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget.setLayout(self.main_layout)

    def create_connections(self):
        # Menubar
        self.pin_window_btn.toggled.connect(self.toggle_always_on_top)
        self.file_open_action.triggered.connect(self.open_video_file)
        # Tabs
        self.video_tabs.tabCloseRequested.connect(lambda index: self.handle_tab_close(index))

    def closeEvent(self, event):
        Config.set(MainWindowVars.position, [self.pos().x(), self.pos().y()])
        Config.set(MainWindowVars.size, [self.width(), self.height()])
        Logger.debug("Saved main window size and position.")
        super().closeEvent(event)

    def add_playback_tab(self, file_path):
        playback_wigdet = PlaybackWidget(file_path)
        tab_title = playback_wigdet.video_file.name
        Logger.debug(tab_title)

    def open_video_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open video file", None)
        if not file_path:
            return

        file_path = pathlib.Path(file_path)
        if not file_path.is_file():
            Logger.error("Not a file: {0}".format(file_path))
            return

        for index in range(self.video_tabs.count()):
            playback_widget: PlaybackWidget = self.video_tabs.widget(index)
            if file_path == playback_widget.video_file.path:
                self.video_tabs.setCurrentIndex(index)
                Logger.warning("File already loaded: {0}".format(file_path))
                return

        new_playback = PlaybackWidget(file_path)
        self.video_tabs.addTab(new_playback, new_playback.video_file.path.name)

    def handle_tab_close(self, index):
        widget: PlaybackWidget = self.video_tabs.widget(index)
        self.video_tabs.removeTab(index)
        widget.media_player.pause()
        widget.deleteLater()

    def toggle_always_on_top(self, state, update=True):
        if state:
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)

        self.pin_window_btn.setChecked(state)
        if update:
            Config.set(MainWindowVars.always_on_top, state)
            self.show()
