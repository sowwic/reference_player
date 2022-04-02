from PySide2 import QtGui
from PySide2 import QtWidgets
from reference_player.widgets.menus.abc_menu import QDMenu


class ToolsMenu(QDMenu):

    TITLE: str = "Tools"

    def create_actions(self):
        self.maya_port_action = QtWidgets.QAction("Command port", self.main_window)
        self.maya_connect_action = QtWidgets.QAction("Connect", self.main_window)
        self.maya_auto_connect_action = QtWidgets.QAction(
            "Auto connect at launch", self.main_window)
        self.maya_auto_connect_action.setCheckable(True)
        self.maya_auto_connect_action.setChecked(self.main_window.config.maya_autoconnect)

    def populate(self):
        maya_separator: QtWidgets.QAction = self.addSeparator()
        maya_separator.setText("Maya")
        self.addAction(self.maya_auto_connect_action)
        self.addAction(self.maya_port_action)
        self.addAction(self.maya_connect_action)
