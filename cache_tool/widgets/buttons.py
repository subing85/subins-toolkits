# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool,  QPushButton wrapper class source code.


from __future__ import absolute_import

import resources

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import utils
from kore import logger

from widgets import PixmapIcon

LOGGER = logger.getLogger(__name__)


class IconButton(QtWidgets.QPushButton):
    name = "icon"
    width = 22
    height = 22

    def __init__(self, parent, **kwargs):
        super(IconButton, self).__init__(parent)

        self.__parent__ = parent

        self.name = kwargs.get("name") or self.name
        self.width = kwargs.get("width") or self.width
        self.height = kwargs.get("height") or self.height
        self.locked = False if kwargs.get("locked") == False else True
        self.flat = kwargs.get("flat") if "flat" in kwargs else True

        self.setToolTip(kwargs.get("toolTip"))

        icon = PixmapIcon(self.name)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(self.width, self.height))

        if self.locked:
            self.setMinimumSize(QtCore.QSize(self.width, self.height))
            self.setMaximumSize(QtCore.QSize(self.width, self.height))


class BrowsePathButton(IconButton):
    name = "browse"

    def __init__(self, parent, **kwargs):
        super(BrowsePathButton, self).__init__(parent)

        self.formats = kwargs.get("formats")
        self.browsepath = kwargs.get("browsepath") or resources.getOrbitPath()
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

        directory = utils.pathResolver(directory)

        LOGGER.info("Directory, %s" % directory)

        if self.widget:
            self.widget.setText(directory)
            self.widget.value = directory

        self.browsepath = directory


class ProjectSaveButton(IconButton):
    name = "save"

    def __init__(self, parent, **kwargs):
        super(ProjectSaveButton, self).__init__(parent)

        self.clicked.connect(self.save)

    def save(self):
        if not self.__parent__.hasValid():
            QtWidgets.QMessageBox.warning(
                self.__parent__,
                "Warning",
                "Invalid project path, update the project path and try!..",
                QtWidgets.QMessageBox.Cancel,
            )
            return

        utils.writeJsonFile(self.__parent__.presetContext, self.__parent__.presetsFilePath)
        LOGGER.info(
            "Succeed, to save your project settings ( %s )" % self.__parent__.presetsFilePath
        )

        QtWidgets.QMessageBox.information(
            self,
            "Information",
            "Succeed, to save your project settings!..",
            QtWidgets.QMessageBox.Ok,
        )


class CacheSaveButton(IconButton):
    name = "save"

    def __init__(self, parent, **kwargs):
        super(CacheSaveButton, self).__init__(parent)

        self.clicked.connect(self.save)

    def save(self):
        if not hasattr(self.__parent__, "widgetItem"):
            return

        values = self.__parent__.getValues()

        self.__parent__.widgetItem.setContext(values, append=True)

        LOGGER.info("Saved your item property")
        for k, v in values.items():
            LOGGER.info("%s: %s" % (k, v))

        self.__parent__.widgetItem.context["save"] = True

        for lineedit, label in self.__parent__.inputWidgets:
            if lineedit.value is None:
                label.setEditColor()
            else:
                label.setSavedColor()

        self.__parent__.updateVersionPath()


class ClearButton(IconButton):
    name = "clear"

    def __init__(self, parent, **kwargs):
        super(ClearButton, self).__init__(parent)

        self.clicked.connect(self.clear)

    def clear(self):
        self.__parent__.reset()


class CacheButton(IconButton):
    name = "alembic"

    def __init__(self, parent, **kwargs):
        super(CacheButton, self).__init__(parent)

        self.setFlat(False)
        self.setText("Publish Cache")
        self.setStyleSheet("text-align: left;")
        self.setMaximumSize(QtCore.QSize(150, 16777215))


if __name__ == "__main__":
    pass
