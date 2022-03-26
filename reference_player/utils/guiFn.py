from PySide2 import QtGui
from PySide2 import QtCore


def get_icon(name):
    """Create QIcon from given name.

    Expects icon to exist under res/images directory

    Args:
        name (str): icon name with extension

    Returns:
        QtGui.QIcon: icon object instance
    """
    return QtGui.QIcon(f"res/images/{name}")


def dark_pallete():
    """Create dark fusion palette.

    Returns:
        QtGui.QPalette: dark palette
    """
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(45, 45, 45))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(208, 208, 208))
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(208, 208, 208))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(208, 208, 208))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(208, 208, 208))
    palette.setColor(QtGui.QPalette.Text, QtGui.QColor(208, 208, 208))
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(45, 45, 48))
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(208, 208, 208))
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.Highlight, QtCore.Qt.gray)

    return palette
