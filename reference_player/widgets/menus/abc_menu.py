from PySide2 import QtWidgets


class QDMenu(QtWidgets.QMenu):

    TITLE: str = "MenuTitle"

    def __init__(self, main_window: QtWidgets.QMainWindow, parent=None):
        super().__init__(self.TITLE, parent)
        self.main_window = main_window

        self.create_actions()
        self.populate()

    def create_actions(self):
        pass

    def populate(self):
        pass
