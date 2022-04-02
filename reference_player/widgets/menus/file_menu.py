from PySide2 import QtGui
from PySide2 import QtWidgets
from reference_player.widgets.menus.abc_menu import QDMenu


class FileMenu(QDMenu):

    TITLE: str = "&File"

    def create_actions(self):
        self.file_new_action = QtWidgets.QAction("&New reference", self.main_window)
        self.file_new_action.setShortcut("Ctrl+N")
        self.file_open_action = QtWidgets.QAction(QtGui.QIcon(
            "open.png"), "&Open reference", self.main_window)
        self.file_open_action.setShortcut("Ctrl+O")
        self.file_open_action.setStatusTip("Open video file")

    def populate(self):
        self.addAction(self.file_new_action)
        self.addAction(self.file_open_action)
