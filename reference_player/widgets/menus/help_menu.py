from PySide2 import QtGui
from PySide2 import QtWidgets

from reference_player import Logger
from reference_player.widgets.menus.abc_menu import QDMenu


class HelpMenu(QDMenu):

    TITLE: str = "Help"

    def create_actions(self):
        self.debug_logging_action = QtWidgets.QAction("Debug logging", self)
        self.debug_logging_action.setCheckable(True)
        self.debug_logging_action.setChecked(Logger.get_level() == 10)
        self.reset_config_action = QtWidgets.QAction("Reset config", self)

    def populate(self):
        self.addAction(self.debug_logging_action)
        self.addAction(self.reset_config_action)
