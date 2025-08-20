# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card) QWidget generic functions.
# WARNING! All changes made in this file will be lost when recompiling UI file!


from __future__ import absolute_import

import os

import resources

import qdarktheme

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets


def setFontSize(widget, size, index=None, family=None, bold=False):
    """Set font size to Qt-widget

    Args:
        widget (object): QtWidgets Class
        size (int): Font size value
        family (str): Optioinal, Type of the font, for example "Arial"
        bold (bool): Optioinal, True if bold fond, False normal font.

    Returns:
        object (QtGui.QFont)

    Examples:
        font = widgets.setFontSize(QtWidgets.QWidget, 14, family="Arial", bold=False)
    """

    index = index or 0

    font = QtGui.QFont()
    font.setPointSize(size)
    if family:
        font.setFamily(family)

    font.setBold(bold)

    if isinstance(widget, QtWidgets.QTreeWidgetItem):
        widget.setFont(index, font)
        return font

    widget.setFont(font)
    return font


def setStylesheet(widget, theme=None):
    """Set the stylesheet to widget

    Args:
        widget (object): QtWidgets Class
        theme (str): optioinal, name of the style, for example "dark" or "light"

    Returns:
        None

    Examples:
        widgets.setStylesheet(QtWidgets.QWidget, widget="dark")
    """

    theme = theme or "dark"  # ['dark', 'light']
    widget.setStyleSheet(qdarktheme.load_stylesheet(theme))


def setImageToButton(button, width, height, iconpath, locked=False):
    """Set the image to QPushButton

    Args:
        button (object): QPushButton
        width (int): Max width of the image to set the button
        height (int): Max height of the image to set the button
        iconpath (str): Icon(image) file path
        locked (bool): Optional, to lock the width and height

    Returns:
        QImage

    Examples:
        widgets.encodeIcon(filepath="test.png")

    """

    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(iconpath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    button.setIcon(icon)
    button.setIconSize(QtCore.QSize(width, height))

    if locked:
        button.setMinimumSize(QtCore.QSize(width, height))
        button.setMaximumSize(QtCore.QSize(width, height))


def setWidgetIcon(widget, iconpath, index=0, width=None, height=None):
    """Set the image to QWidgets items

    Args:
        widget (object): widget class
        iconpath (str): Icon(image) file path
        index (int): Optional, index of the widget to set the icon
        width (int): Optional, max width of the image to set the button
        height (int): Optional, max height of the image to set the button

    Returns:
        QImage

    Examples:
        widgets.setWidgetIcon(trewidgetItem, "test.png", 1, width=25, height=25)

    """

    if not iconpath:
        iconpath = os.path.join(resources.getIconPath(), "unknown.png")

    if isinstance(iconpath, str):
        if not os.path.isfile(iconpath):
            iconpath = os.path.join(resources.getIconPath(), "unknown.png")

    q_image = QtGui.QImage(iconpath)

    if width and height:
        q_image = q_image.scaled(width, height, QtCore.Qt.KeepAspectRatio)

    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(q_image), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    if isinstance(widget, QtWidgets.QMenu):
        widget.setIcon(icon)
    elif isinstance(widget, QtWidgets.QMainWindow) or isinstance(widget, QtWidgets.QWidget):
        widget.setWindowIcon(icon)
    elif isinstance(widget, QtWidgets.QTreeWidgetItem):
        widget.setIcon(index, icon)
    else:
        widget.setIcon(icon)


if __name__ == "__main__":
    pass
