# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)  Resolver QPushButton wrapper source code.
# WARNING! All changes made in this file will be lost when recompiling UI file!

from __future__ import absolute_import

from functools import partial

import widgets
import resources

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import utils
from kore import logger

LOGGER = logger.getLogger(__name__)


class IconButton(QtWidgets.QPushButton):
    name = "icon"
    width = 22
    height = 22

    def __init__(self, parent, **kwargs):
        """This class is inherited from QPushButton and customized for display specific icon(images).

        Args:
            parent (object): parent QtWidget
            width (int): Optional, max width of the icon
            height (int): Optional, max height of the icon
            toolTip (str): Optional, tooltip of the buttion
            locked (bool): Optional,  to lock the width and height
            flat (str): Optional, true if flat button, False normal button.

        Returns:
            None

        Examples:
            iconButton = IconButton(parentWidget)

        """

        super(IconButton, self).__init__(parent)

        self.name = kwargs.get("name") or self.name
        self.width = kwargs.get("w") or self.width
        self.height = kwargs.get("h") or self.height
        self.locked = False if kwargs.get("locked") == False else True
        self.flat = kwargs.get("flat") if "flat" in kwargs else True

        self.iconpath = resources.getIconFilepath(self.name)

        self.setToolTip(kwargs.get("toolTip"))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.iconpath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(self.width, self.height))

        if self.locked:
            self.setMinimumSize(QtCore.QSize(self.width, self.height))
            self.setMaximumSize(QtCore.QSize(self.width, self.height))

        # widgets.setImageToButton(self, self.width, self.height, locked=self.locked, iconpath=self.iconpath)


class TitleButton(IconButton):
    """This class is inherited from Icon button"""

    name = "title"


class DeleteButton(IconButton):
    """this class is inherited from Icon button"""

    name = "delete"


class ResetButton(IconButton):
    """this class is inherited from Icon button"""

    name = "reset"


class ExportButton(IconButton):
    """this class is inherited from Icon button"""

    name = "export"
    width = 100
    height = 32


class CenterAlignButtons(object):
    def __init__(self, parent, layout, **kwargs):
        super(CenterAlignButtons, self).__init__()

        self.__parent__ = parent

        self.align = kwargs.get("align") or "left"

        self.leftButton = IconButton(self.__parent__, name="left")
        self.leftButton.pressed.connect(partial(self.setAlign, "left"))
        layout.addWidget(self.leftButton)

        self.centerButton = IconButton(self.__parent__, name="center")
        self.centerButton.pressed.connect(partial(self.setAlign, "center"))
        layout.addWidget(self.centerButton)

        self.rightButton = IconButton(self.__parent__, name="right")
        self.rightButton.pressed.connect(partial(self.setAlign, "right"))
        layout.addWidget(self.rightButton)

    def setAlign(self, align):
        self.align = align

    def value(self):
        return self.align

    def setValue(self, value):
        self.align = value

    def setDefault(self):
        self.align = "left"

    def deleteLater(self):
        self.leftButton.deleteLater()
        self.centerButton.deleteLater()
        self.rightButton.deleteLater()

    def setVisible(self, value):
        self.leftButton.setVisible(value)
        self.centerButton.setVisible(value)
        self.rightButton.setVisible(value)


class MiddleAlignButtons(object):
    def __init__(self, parent, layout, **kwargs):
        super(MiddleAlignButtons, self).__init__()

        self.align = kwargs.get("align") or "middle"

        self.__parent__ = parent

        self.topButton = IconButton(self.__parent__, name="top")
        self.topButton.pressed.connect(partial(self.setAlign, "top"))
        layout.addWidget(self.topButton)

        self.middleButton = IconButton(self.__parent__, name="middle")
        self.middleButton.pressed.connect(partial(self.setAlign, "middle"))
        layout.addWidget(self.middleButton)

        self.bottomButton = IconButton(self.__parent__, name="bottom")
        self.bottomButton.pressed.connect(partial(self.setAlign, "bottom"))
        layout.addWidget(self.bottomButton)

    def setAlign(self, align):
        self.align = align

    def value(self):
        return self.align

    def setValue(self, value):
        self.align = value

    def setDefault(self):
        self.align = "middle"

    def deleteLater(self):
        self.topButton.deleteLater()
        self.middleButton.deleteLater()
        self.bottomButton.deleteLater()

    def setVisible(self, value):
        self.topButton.setVisible(value)
        self.middleButton.setVisible(value)
        self.bottomButton.setVisible(value)


class AddButton(IconButton):
    """this class is inherited from Icon button"""

    name = "add"


class ShapeButton(QtWidgets.QPushButton):
    """this class is inherited from Icon button"""

    shapes = ["rectangle", "circle"]
    width = 22
    height = 22

    def __init__(self, parent, **kwargs):
        super(ShapeButton, self).__init__(parent)

        self.width = kwargs.get("w") or self.width
        self.height = kwargs.get("h") or self.height
        self.locked = False if kwargs.get("locked") == False else True
        self.flat = kwargs.get("flat") if "flat" in kwargs else True

        self.shape = self.shapes[0]

        self.setIcons()

        self.clicked.connect(self.setValue)

    def setIcons(self, locked=False):
        iconPath = resources.getIconFilepath(self.shape)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(self.width, self.height))

        if self.locked:
            self.setMinimumSize(QtCore.QSize(self.width, self.height))
            self.setMaximumSize(QtCore.QSize(self.width, self.height))

    def setValue(self, locked=False):
        index = self.shapes.index(self.shape)
        if len(self.shapes) <= index + 1:
            index = 0
        else:
            index = index + 1
        self.shape = self.shapes[index]
        self.setIcons(locked=locked)

    def value(self):
        return self.shape

    def setDefault(self):
        self.shape = self.shapes[0]
        self.setIcons()


class ColorButton(QtWidgets.QPushButton):
    name = "color"

    def __init__(self, parent, **kwargs):
        """This class is inherited from QPushButton and customized for display specific icon(images).

        Args:
            parent (object): parent QtWidget
            width (int): Optional, max width of the icon
            height (int): Optional, max height of the icon
            toolTip (str): Optional, tooltip of the buttion
            locked (bool): Optional,  to lock the width and height
            flat (str): Optional, true if flat button, False normal button.

        Returns:
            None

        Examples:
            iconButton = IconButton(parentWidget)

        """

        super(ColorButton, self).__init__(parent)

        self.name = kwargs.get("name") or self.name
        self.width = kwargs.get("w", 22)
        self.height = kwargs.get("h", 22)
        self.locked = False if kwargs.get("locked") == False else True
        self.flat = kwargs.get("flat") if "flat" in kwargs else True

        self.color = kwargs.get("color") or (0, 0, 0)
        self.rgb = QtGui.QColor(*self.color)
        self.colorName = self.rgb.name()

        self.setToolTip(kwargs.get("toolTip"))

        self.setStyleSheet(
            "background-color: rgb(%s, %s, %s);" % (self.color[0], self.color[1], self.color[2])
        )

        if self.locked:
            self.setMinimumSize(QtCore.QSize(self.width, self.height))
            self.setMaximumSize(QtCore.QSize(self.width, self.height))

        self.clicked.connect(self.setColor)

        # widgets.setImageToButton(self, self.width, self.height, locked=self.locked, iconpath=self.iconpath)

    def setColor(self):
        colorQt = QtWidgets.QColorDialog.getColor()

        self.color = colorQt.red(), colorQt.green(), colorQt.blue()
        self.colorName = colorQt.name()

        self.setStyleSheet(
            "background-color: rgb(%s, %s, %s);" % (self.color[0], self.color[1], self.color[2])
        )
        print("self.colorName", self.colorName)

        return colorQt

    def value(self):
        # return self.color
        return self.colorName

    def setValue(self, value):
        colorQt = QtGui.QColor(value)
        self.color = colorQt.red(), colorQt.green(), colorQt.blue()
        self.colorName = colorQt.name()

        self.setStyleSheet(
            "background-color: rgb(%s, %s, %s);" % (self.color[0], self.color[1], self.color[2])
        )


class BrowseFileButton(IconButton):
    """this class is inherited from Icon button"""

    name = "browse"

    def __init__(self, parent, **kwargs):
        super(BrowseFileButton, self).__init__(parent)

        self.__parent__ = parent

        self.formats = kwargs.get("formats")
        self.browsepath = kwargs.get("browsepath") or resources.getProjectPath()
        self.widget = kwargs.get("widget")

        self.clicked.connect(self.findFile)

    def findFile(self):
        fileDialog = QtWidgets.QFileDialog(self.__parent__)

        formatPattern = "(*" + " *".join(self.formats) + ")"
        filepath, format = fileDialog.getOpenFileName(
            self.__parent__, "Browse your file", self.browsepath, formatPattern
        )

        if not filepath:
            return

        LOGGER.info("file path, %s %s" % (filepath, format))

        if self.widget:
            self.widget.clear()
            self.widget.setText(utils.pathResolver(filepath))

        self.browsepath = utils.dirname(filepath)


class BrowsePathButton(IconButton):
    name = "browse"

    def __init__(self, parent, **kwargs):
        super(BrowsePathButton, self).__init__(parent)

        self.__parent__ = parent

        self.formats = kwargs.get("formats")
        self.browsepath = kwargs.get("browsepath") or resources.getProjectPath()
        self.widget = kwargs.get("widget")

        self.clicked.connect(self.findFile)

    def findFile(self):
        fileDialog = QtWidgets.QFileDialog(self.__parent__)

        directory = fileDialog.getExistingDirectory(
            self.__parent__,
            "Browse your file",
            self.browsepath,
            QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks,
        )

        if not directory:
            return

        LOGGER.info("Directory, %s" % directory)

        if self.widget:
            self.widget.clear()
            self.widget.setText(utils.pathResolver(directory))

        self.browsepath = directory


class DiagramButton(QtWidgets.QPushButton):
    def __init__(self, parent, **kwargs):
        super(DiagramButton, self).__init__(parent)

        self.__parent__ = parent

        self.pixmap = None
        self.locked = False if kwargs.get("locked") == False else True

        self.flat = kwargs.get("flat") if "flat" in kwargs else True
        self.zoom = 0
        self.increment = 2

        self.iconpath = resources.getIconFilepath("background")

        self.setToolTip(kwargs.get("toolTip"))

        # ==============================================
        # How to Convert Inch to Pixel (X)
        # 1 in = 96 pixel (X)
        # 1 pixel (X) = 0.0104166667 in
        # Example: convert 15 in to pixel (X):
        # 15 in = 15 × 96 pixel (X) = 1440 pixel (X)
        # ==============================================
        # self.setBackground(None, locked=self.locked)

    def _setBackground(self, iconpath, locked=False):
        iconpath = iconpath or self.iconpath
        self.setDiagram(QtGui.QPixmap(iconpath), locked=locked)

    def setDisplay(self, zoom=None, locked=False):
        self.zoom = self.zoom if zoom is None else zoom

        if self.pixmap.width() < self.pixmap.height():
            scaledPixmap = self.pixmap.scaledToWidth(
                (self.pixmap.width() + self.zoom), mode=QtCore.Qt.SmoothTransformation
            )
        else:
            scaledPixmap = self.pixmap.scaledToHeight(
                (self.pixmap.height() + self.zoom), mode=QtCore.Qt.SmoothTransformation
            )

        icon = QtGui.QIcon()
        icon.addPixmap(scaledPixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(icon)

        self.setIconSize(scaledPixmap.size())

        if locked:
            self.setMinimumSize(scaledPixmap.size())
            self.setMaximumSize(scaledPixmap.size())

    def setDiagram(self, pixmap, locked=False):
        self.pixmap = pixmap or QtGui.QPixmap(self.iconpath)
        self.setDisplay(locked=locked)

    def setResultion(self, width, height, locked=False):
        self.width, self.height = int(width), int(height)

        self.setIconSize(QtCore.QSize(self.width, self.height))

        if locked:
            self.setMinimumSize(QtCore.QSize(self.width, self.height))
            self.setMaximumSize(QtCore.QSize(self.width, self.height))


class RenderButton(QtWidgets.QPushButton):
    def __init__(self, parent, **kwargs):
        super(RenderButton, self).__init__(parent)

        self.setText("Render")


if __name__ == "__main__":
    pass
