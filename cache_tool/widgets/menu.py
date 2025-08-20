# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, QMenu wrapper class source code.

from __future__ import absolute_import

from functools import partial

import resources

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import utils
from kore import logger
from kore import constant

from widgets import PixmapIcon
from widgets import SetStylesheet

LOGGER = logger.getLogger(__name__)


class ToolbarMenu(QtWidgets.QToolBar):
    def __init__(self, parent, **kwargs):
        super(ToolbarMenu, self).__init__(parent)

        self.__parent__ = parent

        self.logs = False
        self.saveFilepath = None

        self.addItemAction = AddItemAction(self)
        self.addAction(self.addItemAction)
        self.addSeparator()

        self.realoadtemAction = ReloadItemAction(self)
        self.addAction(self.realoadtemAction)
        self.addSeparator()

        self.removeItemAction = RemoveItemAction(self)
        self.addAction(self.removeItemAction)
        self.addSeparator()

        self.removeAllItemAction = RemoveAllItemAction(self)
        self.addAction(self.removeAllItemAction)
        self.addSeparator()

        self.publishCacheAllAction = PublishCacheAllAction(self)
        self.addAction(self.publishCacheAllAction)

        spacerWidget = QtWidgets.QWidget()
        spacerWidget.setWindowOpacity(0)
        spacerWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.addWidget(spacerWidget)

        self.themeAction = ThemeAction(self)
        self.addAction(self.themeAction)

        self.addSeparator()

        self.priorityMenu = PriorityMenu(self)
        self.addAction(self.priorityMenu.menuAction())

        self.displayLoggerAction = DisplayLoggerAction(self)
        self.addAction(self.displayLoggerAction)

        self.addSeparator()
        self.helpAction = HelpAction(self)
        self.addAction(self.helpAction)


class NormalMenu(QtWidgets.QMenu):
    label = "normal"
    name = "normal"
    toolTip = "normal"

    def __init__(self, parent, **kwargs):
        super(NormalMenu, self).__init__(parent)

        self.__parent__ = parent

        self.setTitle(self.label)
        self.setToolTip(self.toolTip)

        icon = PixmapIcon(self.name)
        self.setIcon(icon)


class CpuCountMenu(NormalMenu):
    label = "cpu"
    name = "cpu"
    toolTip = "Set processer thread count"

    def __init__(self, parent, **kwargs):
        super(CpuCountMenu, self).__init__(parent)

        self.setTearOffEnabled(True)

        threadReadPool = QtCore.QThreadPool()
        maxThreadCount = threadReadPool.maxThreadCount()

        self.actionList = list()

        for count in range(maxThreadCount):
            action = QtWidgets.QAction(self)
            action.setText("CPU %s" % str(count))
            action.setCheckable(True)
            action.setChecked(True)
            self.addAction(action)
            self.actionList.append(action)


class PriorityMenu(NormalMenu):
    label = "priority"
    name = "priority"
    toolTip = "Set the Priority"

    def __init__(self, parent, **kwargs):
        super(PriorityMenu, self).__init__(parent)

        self.setTearOffEnabled(True)

        priorityList = [
            [
                "Realtime",
                QtCore.QThread.HighestPriority,
                5,
                "Scheduled more often than HighPriority.",
            ],
            ["High", QtCore.QThread.HighPriority, 4, "Scheduled more often than NormalPriority."],
            [
                "Above Normal",
                QtCore.QThread.NormalPriority,
                3,
                "The default priority of the operating system.",
            ],
            [
                "Below Normal",
                QtCore.QThread.LowPriority,
                2,
                "Scheduled less often than NormalPriority.",
            ],
            ["Low", QtCore.QThread.LowestPriority, 1, "Scheduled less often than LowPriority."],
        ]

        self.actionList = list()

        for label, qthread, index, toolTip in priorityList:
            action = QtWidgets.QAction(self)
            action.setText(label)
            action.setToolTip(toolTip)
            action.setCheckable(True)
            self.addAction(action)
            action.triggered.connect(partial(self.setPriority, action, index, qthread))
            self.actionList.append(action)

        self.actionList[0].setChecked(True)

    def setPriority(self, action, index, qthread):
        for each in self.actionList:
            if each == action:
                continue
            each.setChecked(False)

        self.__parent__.__parent__.priority = qthread
        LOGGER.info("Priority change into, %s ( %s )" % (index, qthread))


class NormalAction(QtWidgets.QAction):
    label = "normal"
    name = "normal"
    toolTip = "normal"

    def __init__(self, parent, **kwargs):
        super(NormalAction, self).__init__(parent)
        self.__parent__ = parent

        self.setText(self.label)
        self.setToolTip(self.toolTip)

        icon = PixmapIcon(self.name)
        self.setIcon(icon)


class AddItemAction(NormalAction):
    label = "addItem"
    name = "add-item"
    toolTip = "Add new Item"

    def __init__(self, parent, **kwargs):
        super(AddItemAction, self).__init__(parent)

        self.browsepath = kwargs.get("browsepath") or resources.getOrbitPath()

        self.triggered.connect(self.addItem)

    def addItem(self):
        fileDialog = QtWidgets.QFileDialog(self.__parent__.__parent__)
        filepaths, format = fileDialog.getOpenFileNames(
            self.__parent__.__parent__,
            "Browse your source files",
            self.browsepath,
            "Maya/Blender file (*.%s)" % " *.".join(constant.INPUT_EXTENTIONS),
        )

        self.__parent__.__parent__.fileTreewidget.addFileItems(filepaths)

        self.browsepath = utils.dirname(filepaths[0])


class ReloadItemAction(NormalAction):
    label = "reload"
    name = "reload"
    toolTip = "Remove selected item"

    def __init__(self, parent, **kwargs):
        super(ReloadItemAction, self).__init__(parent)

        self.triggered.connect(self.reloadItem)

    def reloadItem(self):
        selectedItems = self.__parent__.__parent__.fileTreewidget.selectedItems()
        currentItem = selectedItems[0] if selectedItems else None

        if not currentItem:
            QtWidgets.QMessageBox.warning(
                self.__parent__.__parent__,
                "Warning",
                "Could not found any selection, please select the item and try!..",
                QtWidgets.QMessageBox.Cancel,
            )
            return

        if not currentItem.hasSourceItem():
            currentItem = currentItem.parent()

        self.__parent__.__parent__.fileTreewidget.readItem(currentItem)


class RemoveItemAction(NormalAction):
    label = "remove"
    name = "remove"
    toolTip = "Remove selected item"

    def __init__(self, parent, **kwargs):
        super(RemoveItemAction, self).__init__(parent)

        self.triggered.connect(self.removeItem)

    def removeItem(self):
        selectedItems = self.__parent__.__parent__.fileTreewidget.selectedItems()
        currentItem = selectedItems[0] if selectedItems else None

        if not currentItem:
            QtWidgets.QMessageBox.warning(
                self.__parent__.__parent__,
                "Warning",
                "Could not found any selection, please select the item and try!..",
                QtWidgets.QMessageBox.Cancel,
            )
            return

        if not currentItem.hasSourceItem():
            currentItem = currentItem.parent()

        self.__parent__.__parent__.fileTreewidget.removeItems(currentItem)


class RemoveAllItemAction(NormalAction):
    label = "removeAll"
    name = "remove-all"
    toolTip = "Remove all Item"

    def __init__(self, parent, **kwargs):
        super(RemoveAllItemAction, self).__init__(parent)

        self.triggered.connect(self.removeAllItem)

    def removeAllItem(self):
        self.__parent__.__parent__.fileTreewidget.removeAllItems()


class PublishCacheAllAction(NormalAction):
    label = "cacheAll"
    name = "cache-all"
    toolTip = "Publish cache all"

    def __init__(self, parent, **kwargs):
        super(PublishCacheAllAction, self).__init__(parent)

        self.triggered.connect(self.publishCacheAll)

    def publishCacheAll(self):
        self.__parent__.__parent__.fileTreewidget.cacheItAll()


class HelpAction(NormalAction):
    label = "help"
    name = "help"
    toolTip = "About the appliction"

    def __init__(self, parent, **kwargs):
        super(HelpAction, self).__init__(parent)

        self.triggered.connect(self.openHelp)

    def openHelp(self):
        LOGGER.info("More deatils, please look at this page: %s" % constant.HELP_URL)
        utils.openUrl(constant.HELP_URL)


class DisplayLoggerAction(NormalAction):
    label = "logger"
    name = "logger-disabled"
    toolTip = "Display detailed logs"

    def __init__(self, parent, **kwargs):
        super(DisplayLoggerAction, self).__init__(parent)

        self.display = False

        self.triggered.connect(self.displayLogger)

    def setActive(self, display):
        self.name = "logger-disabled" if display else "logger-normal"

        self.iconpath = resources.getIconFilepath(self.name)

        icon = PixmapIcon(self.name)
        self.setIcon(icon)

        self.display, mode = (False, "Off") if self.display else (True, "On")

        LOGGER.info("Display logs mode, %s" % mode)

    def displayLogger(self):
        self.setActive(self.display)
        self.__parent__.__parent__.fileTreewidget.setDisplayLogs(self.display)
        self.__parent__.__parent__.cachePropertyPage.setDisplayLogs(self.display)


class ThemeAction(NormalAction):
    label = "theme"
    name = "theme"
    toolTip = "Switch to theme"

    def __init__(self, parent, **kwargs):
        super(ThemeAction, self).__init__(parent)

        self.themes = constant.GUI_THEMES
        self.theme = constant.GUI_THEMES[0]

        self.triggered.connect(self.switchTheme)

    def switchTheme(self):
        self.theme = self.themes[1] if self.theme == self.themes[0] else self.themes[0]
        SetStylesheet(self.__parent__.__parent__, theme=self.theme)


if __name__ == "__main__":
    pass
