# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, QTreeWidget wrapper class source code.


from __future__ import absolute_import

import resources

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import utils
from kore import batch
from kore import logger
from kore import thread
from kore import constant

from widgets.widgetItems import FileWidgetItem
from widgets.widgetItems import NodeWidgetItem

LOGGER = logger.getLogger(__name__)


class NormalTreewidget(QtWidgets.QTreeWidget):
    iconSize = (72, 72)

    def __init__(self, parent, *args, **kwargs):
        super(NormalTreewidget, self).__init__(parent)

        self.__parent__ = parent

        self.setHeaderHidden(True)
        self.setSortingEnabled(False)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.setIconSize(QtCore.QSize(self.iconSize[0], self.iconSize[1]))


class FileTreewidget(NormalTreewidget):
    changed = QtCore.Signal()

    iconSize = (42, 42)

    def __init__(self, parent, *args, **kwargs):
        super(FileTreewidget, self).__init__(parent)

        self.context = dict()
        self.childItems = list()
        self.cachePropertyPage = None
        self.displayLogs = False

        self.setAcceptDrops(True)
        self.setColumnCount(1)

        self.setIconSize(QtCore.QSize(self.iconSize[0], self.iconSize[1]))

        self.sortByColumn(0, QtCore.Qt.AscendingOrder)

        self.itemClicked.connect(self.loadProperty)

    def setDisplayLogs(self, value):
        self.displayLogs = value

    def getWidgetItems(self):
        widgetItems = list()
        treewidget = self.invisibleRootItem()
        for index in range(treewidget.childCount()):
            path = treewidget.child(index).toolTip(1)
            widgetItems.append(path)
        return widgetItems

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if not mimeData.hasUrls():
            return

        filepaths = list()
        for url in mimeData.urls():
            filepaths.append(utils.pathResolver(url.toLocalFile()))

        self.addFileItems(filepaths)

        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        event.accept()

    def setChildItems(self, item):
        self.childItems.append(item)

    def hasItemExists(self, filepath):
        context = list(filter(lambda x: x.filepath == filepath, self.childItems))
        return True if context else False

    def hasValuedFile(self, filepath):
        extenstion = utils.fileExtenstion(filepath)
        return True if extenstion in self.__parent__.projectGroup.validExtensions else False

    def hasRunning(self, widgetItems=None):
        widgetItems = widgetItems or self.childItems

        for widgetItem in widgetItems:
            if widgetItem.hasThreading():
                LOGGER.warning("Running, please try after completed")
                running = True
                break
        else:
            running = False

        return running

    def removeItems(self, widgetItems):
        if not isinstance(widgetItems, list):
            widgetItems = [widgetItems]

        parentWidgetItem = self.invisibleRootItem()
        for widgetItem in widgetItems:
            if self.hasRunning(widgetItems=[widgetItem]):
                LOGGER.warning("Running, please try after completed")
                continue

            self.childItems.remove(widgetItem)
            parentWidgetItem.removeChild(widgetItem)

    def removeAllItems(self):
        if self.hasRunning(widgetItems=None):
            return

        self.clear()
        self.childItems = list()

    def getProjectContext(self, filepath):
        extenstion = utils.fileExtenstion(filepath)

        projectContextList = list(
            filter(
                lambda x: x.get("extensions") and extenstion in x["extensions"],
                self.__parent__.projectGroup.projectContextList,
            )
        )

        return projectContextList[0].copy() if projectContextList else None

    def addFileItems(self, filepaths):
        if isinstance(filepaths, str):
            filepaths = [filepaths]

        for filepath in filepaths:
            if not self.hasValuedFile(filepath):
                LOGGER.warning("Invalid file format, %s" % filepath)
                continue

            if self.hasItemExists(filepath):
                LOGGER.warning("Already exists, %s" % filepath)
                continue

            projectContext = self.getProjectContext(filepath)

            fileWidgetItem = FileWidgetItem(self, projectContext["name"], filepath)
            fileWidgetItem.setContext(projectContext, append=False)

            self.importItem(fileWidgetItem)
            self.setChildItems(fileWidgetItem)

    def importItem(self, widgetItem):
        widgetItem.setDisplay(1)
        widgetItem.setThreading(True)

        inputs = widgetItem.context.copy()

        fileReadWorker = thread.WorkerImportRunner(
            self.importSourceFile, widgetItem.filepath, self.displayLogs, widgetItem, **inputs
        )
        fileReadWorker.signals.progress.connect(self.importThreadProgress)
        fileReadWorker.signals.error.connect(self.importThreadError)
        fileReadWorker.signals.finished.connect(self.importThreadFinished)

        self.__parent__.threadReadPool.start(
            fileReadWorker,
            priority=self.__parent__.priority,  # QtCore.QThread.HighestPriority
        )

    def importSourceFile(self, filepath, *args, **kwargs):
        logger.nextLine()
        LOGGER.info("Started import %s file" % kwargs["name"])
        LOGGER.info("Current priority, %s" % self.__parent__.priority)
        LOGGER.info("Source filepath, %s" % filepath)

        logger.nextLine()

        LOGGER.info("Input context")
        for k, v in kwargs.items():
            LOGGER.info("%s: %s" % (k, v))

        logger.nextLine()

        self.importFile = batch.ImportFile()
        context = self.importFile.doIt(filepath, **kwargs)

        return context

    def importThreadProgress(self, result):
        LOGGER.info(result)

    def importThreadFinished(self, inputs):
        widget = inputs["widget"]
        context = inputs["context"]

        widget.setThreading(False)

        LOGGER.info("Display logs mode, %s" % self.displayLogs)

        if not context["valid"]:
            widget.setDisplay(0)
            LOGGER.error(
                "Python script snippet failure (%s file subprocess failure)." % widget.name
            )
            return

        if not context["result"]:
            widget.setDisplay(0)
            LOGGER.error("Unexpected %s file." % widget.name)
            return

        if not context["result"].get("nodes"):
            widget.setDisplay(0)
            LOGGER.error("Could find expected %s cache groups." % widget.name)
            return

        context["isRead"] = True

        widget.setContext(context, append=True)

        if widget.childItems:
            for child in widget.childItems:
                widget.removeChild(child)

        for node in context["result"]["nodes"]:
            nodeWidgetItem = NodeWidgetItem(widget, constant.NODE_ICON_NAME, node)
            widget.setExpanded(True)
            widget.setChild(nodeWidgetItem)

        widget.setDisplay(2)

        LOGGER.error("%s thread finished." % widget.name)

    def importThreadError(self, error):
        exctype, value, traceback, widget = error
        print(exctype)
        print(value)
        print(traceback)
        widget.setDisplay(0)

    def loadProperty(self, item, column):
        currentItem = self.selectedItems()[-1] if self.selectedItems() else None

        if not currentItem.isRead:
            return

        self.__parent__.cachePropertyPage.reset()

        if not currentItem:
            self.__parent__.cachePropertyPage.setEnabled(False)
            LOGGER.warning("Could not found any selected item")
            return

        if currentItem.hasChild():
            currentItem = currentItem.parent()

        self.__parent__.cachePropertyPage.setEnabled(True)
        self.__parent__.cachePropertyPage.setWidgetItem(currentItem)

        result = currentItem.context.get("result")

        self.__parent__.cachePropertyPage.setValues(result)
        self.__parent__.toolBox.setCurrentIndex(0)
        self.__parent__.toolBox.setItemText(0, "Cache Property ( %s )" % currentItem.filepath)

    def cacheItAll(self):
        if self.hasRunning(widgetItems=None):
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "Please wait until import all items and try",
                QtWidgets.QMessageBox.Cancel,
            )
            return

        contextItems = [child for child in self.childItems if child.context.get("save")]

        if not contextItems:
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "Could not found any saved Cache property!..\nSave and try",
                QtWidgets.QMessageBox.Cancel,
            )
            return

        for child in contextItems:
            self.__parent__.cachePropertyPage.setWidgetItem(child)
            self.__parent__.cachePropertyPage.cacheIt(diaplayMessageBox=False)

    def localPathExists(self, localPath, widgetItem=None):
        for child in self.childItems:
            if child == widgetItem:
                continue
            if child.context.get("localPath") and child.context["localPath"] == localPath:
                result = True
                break
        else:
            result, child = False, None

        return result, child


if __name__ == "__main__":
    pass
