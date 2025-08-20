# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)  Resolver QTreeWidget wrapper source code.
# WARNING! All changes made in this file will be lost when recompiling UI file!


from __future__ import absolute_import

import copy

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets


from kore import utils
from kore import logger
from kore import constants

LOGGER = logger.getLogger(__name__)


class NormalTreewidget(QtWidgets.QTreeWidget):
    iconSize = (72, 72)

    def __init__(self, parent, *args, **kwargs):
        super(NormalTreewidget, self).__init__(parent)

        self.__parent__ = parent

        self.setHeaderHidden(False)
        self.setSortingEnabled(False)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.setIconSize(QtCore.QSize(self.iconSize[0], self.iconSize[1]))

        self.header().setStretchLastSection(True)


class OutlineTreewidget(NormalTreewidget):
    def __init__(self, parent, *args, **kwargs):
        super(OutlineTreewidget, self).__init__(parent)

        self.filepath = None
        self.projectPath = None
        self.imagesPath = None
        self.children = list()
        self.headerList = list()

        self.setHeaderHidden(True)
        # self.headerItem().setText(0, "")

    def clean(self):
        self.clear()

        self.filepath = None
        self.projectPath = None
        self.imagesPath = None
        self.children = list()
        self.headerList = list()
        self.__parent__.hasLoadedOutlineItems = False

    def setChildren(self, child):
        self.children.append(child)

    def setHeaderItems(self, values):
        self.setHeaderHidden(False)
        self.setColumnCount(len(values))
        self.headerItem().setText(0, "Icon")

        # font = QtGui.QFont()
        font = self.headerItem().font(0)
        font.setPointSize(12)
        font.setBold(True)

        # brush = QtGui.QBrush(QtGui.QColor(85, 170, 255))
        brush = self.headerItem().foreground(0)
        brush.setColor(QtGui.QColor(85, 170, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)

        self.headerItem().setFont(0, font)
        self.headerItem().setForeground(0, brush)

        for index, value in enumerate(values):
            self.headerItem().setFont(index + 1, font)
            self.headerItem().setForeground(index + 1, brush)

            self.headerItem().setText(index + 1, value)
            self.header().resizeSection(index + 1, len(value) * 50)

    def getContextList(self):
        contextList = list()
        for x, child in enumerate(self.children):
            context = {
                "index": child.index,
                "inputContext": child.inputContext,
                "barcodeContext": child.barcodeContext,
                "fieldContextList": child.fieldContextList,
                "treeContext": child.context,
            }
            contextList.append(context)
        return contextList

    def getPathContext(self):
        context = {
            "filepath": self.filepath,
            "projectPath": self.projectPath,
            "imagesPath": self.imagesPath,
        }

        return context

    def loadItem(self, filepath, inputContext, barcodeContext, fieldContextList):
        self.filepath = filepath
        self.projectPath = utils.dirname(self.filepath)
        self.imagesPath = utils.pathResolver(self.projectPath, folders=[constants.IMAGES])

        contextList = utils.importCSV(filepath)

        self.clear()

        self.headerList = list(contextList[0].keys())

        self.setHeaderItems(self.headerList)

        for index, context in enumerate(contextList):
            childWidgetItem = OutlineChildWidgetItem(
                self, self.projectPath, self.filepath, self.imagesPath
            )
            childWidgetItem.setItems(context, inputContext, barcodeContext, fieldContextList)
            childWidgetItem.setIndex(index)
            self.setChildren(childWidgetItem)

        self.__parent__.hasLoadedOutlineItems = True

        self.__parent__.renderGroup.setDefaultValues()

        # self.itemDoubleClicked.connect(self.launchApplication)
        self.itemClicked.connect(self.loadTo)

    def loadTo(self, currentItem):
        if currentItem.typed != "child":
            return
        self.__parent__.setCurrentOutlineItem(currentItem)

        currentItem.loadTo()

    def loadCurrentContext(self, pathContext, contextList):
        if not utils.hasFileExists(pathContext["filepath"]):
            return False, "CSV file missing, could not found ( %s ) file" % pathContext["filepath"]

        self.loadItem(
            utils.pathResolver(pathContext["filepath"]),
            self.__parent__.inputGroup.inputContext,
            self.__parent__.fieldGroup.fieldContextList,
        )

        for child in self.children:
            context_list = list(filter(lambda x: x["index"] == child.index, contextList))
            if not context_list:
                continue

            child.inputContext = context_list[0]["inputContext"]
            child.fieldContextList = context_list[0]["fieldContextList"]


class NormalWidgetItem(QtWidgets.QTreeWidgetItem):
    typed = None

    def __init__(self, parent, *args, **kwargs):
        super(NormalWidgetItem, self).__init__(parent)

        self.__parent__ = parent

        self.value = None
        self.index = None
        self.filepath = None
        self.context = dict()
        self.contextList = list()

        self.setFlags(
            QtCore.Qt.ItemIsSelectable
            | QtCore.Qt.ItemIsDropEnabled
            | QtCore.Qt.ItemIsUserCheckable
            | QtCore.Qt.ItemIsEnabled
        )

    def setContext(self, context):
        self.context = context
        self.contextList = list(context.values())
        for k, v in context.items():
            key = k.replace("-", "_") if "-" in k else k
            setattr(self, key, v)

    def setContextList(self, contextList):
        self.contextList = contextList

    def setIndex(self, index):
        self.index = index

    def setFilepath(self, filepath):
        self.filepath = filepath

    def setToolTips(self, toolTips, index=None):
        index = 0 if index is None else index
        self.setToolTip(index, toolTips)

    def setValue(self, value, index=None):
        index = 0 if index is None else index
        self.setText(index, value)
        self.value = value

    def setFontProperty(self, index, size, bold=False, family=None, color=None):
        font = QtGui.QFont()
        font.setPointSize(size)
        if family:
            font.setFamily(family)

        font.setBold(bold)
        self.setFont(index, font)

        if color:
            self.setForegroundColor(color, index=index)

    def setForegroundColor(self, color, index=None):
        if isinstance(color, str):
            qcolor = QtGui.QColor(color)
        else:
            qcolor = QtGui.QColor(color[0], color[1], color[2])

        if isinstance(index, int):
            indexList = [index]
        else:
            indexList = list(range(self.treeWidget().columnCount()))

        for index in indexList:
            brush = self.foreground(index)
            brush.setColor(qcolor)
            brush.setStyle(QtCore.Qt.SolidPattern)
            self.setForeground(index, brush)

    def setThumbnail(self, filepath, index=None, width=None, height=None):
        index = index or 0

        q_image = QtGui.QImage(filepath)

        if width and height:
            q_image = q_image.scaled(width, height, QtCore.Qt.KeepAspectRatio)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(q_image), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(index, icon)

    def remove(self):
        widgetItem = self.treeWidget().invisibleRootItem()
        widgetItem.removeChild(self)


class OutlineChildWidgetItem(NormalWidgetItem):
    typed = "child"
    iconSize = (72, 72)

    def __init__(self, parent, *args, **kwargs):
        super(OutlineChildWidgetItem, self).__init__(parent)

        self.projectPath = args[0]
        self.filepath = args[1]
        self.imagesPath = args[2]
        self.iconFilepath = None
        self.iconFilename = None

        self.inputContext = dict()
        self.fieldContextList = list()

    def setItems(self, context, inputContext, barcodeContext, fieldContextList):
        self.setContext(context)

        self.iconFilepath, self.iconFilename = utils.imageFile(
            utils.pathResolver(self.imagesPath, filename=self.context["image"])
        )

        self.setThumbnail(
            self.iconFilepath, index=0, width=self.iconSize[0], height=self.iconSize[1]
        )

        for index, each in enumerate(context):
            self.setValue(context[each], index=index + 1)
            self.setFontProperty(index + 1, 10, bold=False, color=(255, 255, 255))

        self.inputContext = copy.deepcopy(inputContext)
        self.barcodeContext = copy.deepcopy(barcodeContext)
        self.fieldContextList = copy.deepcopy(fieldContextList)

        self.inputContext["foreground"]["default"] = self.iconFilepath

        if self.barcodeContext and self.context.get("barcode"):
            self.barcodeContext["text"]["default"] = self.context["barcode"].replace(" ", "-")

        for fieldContext in self.fieldContextList:
            for k, values in fieldContext.items():
                if k == "field" and values["default"] in self.context:
                    fieldContext["text"]["default"] = self.context[values["default"]]

                fieldContext[k]["default"] = values["default"]

    def loadTo(self):
        filepath, filename = utils.imageFile(
            utils.pathResolver(self.imagesPath, filename=self.context["image"])
        )

        # self.__parent__.__parent__.imagesPath = self.imagesPath
        self.inputContext["foreground"]["default"] = filepath
        # self.inputContext["background"]["default"] = self.inputContext["background"]["default"]

        # self.__parent__.__parent__.diagramGroup.layer.clear()
        self.__parent__.__parent__.inputGroup.clear()
        self.__parent__.__parent__.barcodeGroup.clear()
        self.__parent__.__parent__.fieldGroup.clear()

        self.__parent__.__parent__.inputGroup.setValues(self.inputContext)
        self.__parent__.__parent__.barcodeGroup.setValues(self.barcodeContext)
        self.__parent__.__parent__.fieldGroup.setValues(self.fieldContextList)

        # self.__parent__.__parent__.setDiagram()

    def setOverrideInputContext(self, inputs):
        for k, v in inputs.items():
            if k not in self.inputContext:
                continue
            if v == self.inputContext[k]["default"]:
                continue

            self.inputContext[k]["value"] = v

    def setOverrideBarcodeContext(self, inputs):
        for k, v in inputs.items():
            if k not in self.barcodeContext:
                continue
            if v == self.barcodeContext[k]["default"]:
                continue

            self.barcodeContext[k]["value"] = v

    def setOverrideFieldContext(self, index, inputs):
        for k, v in inputs.items():
            if k not in self.fieldContextList[index]:
                continue
            if v == self.fieldContextList[index][k]["default"]:
                continue

            self.fieldContextList[index][k]["value"] = v


if __name__ == "__main__":
    pass
