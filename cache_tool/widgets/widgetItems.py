# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, QTreeWidget wrapper source code.

from __future__ import absolute_import

import resources

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import logger

from widgets import Font
from widgets import PixmapIcon

LOGGER = logger.getLogger(__name__)


class NormalWidgetItem(QtWidgets.QTreeWidgetItem):
    fontsize = 10
    bold = False

    def __init__(self, parent, *args, **kwargs):
        super(NormalWidgetItem, self).__init__(parent)

        self.__parent__ = parent

        self.name = args[0]
        self.typed = None
        self.value = None
        self.index = None
        self.filepath = None
        self.context = dict()

        self.iconpath = resources.getIconFilepath(self.name)

        icon = PixmapIcon(self.name)
        self.setIcon(0, icon)

        font = Font(self.fontsize, family="Arial", bold=self.bold)
        self.setFont(0, font)

        self.setCheckState(0, QtCore.Qt.Checked)

    def setContext(self, context, append=False):
        if append:
            self.context.update(context)
        else:
            self.context = context

        self.contextList = list(self.context.values())
        for k, v in context.items():
            setattr(self, k, v)


class FileWidgetItem(NormalWidgetItem):
    fontsize = 10
    bold = True

    def __init__(self, parent, *args, **kwargs):
        super(FileWidgetItem, self).__init__(parent, *args, **kwargs)

        self.name = args[0]
        self.filepath = args[1]

        self.childItems = list()

        self.isRead = None
        self.isCached = None
        self.thread = False

        self.context = {"filepath": args[0], "isRead": False}

        self.setDisplay(1)

    def hasSourceItem(self):
        return True

    def setChild(self, child):
        self.childItems.append(child)

    def hasChild(self):
        return False

    def hasChecked(self):
        if self.checkState(0) == QtCore.Qt.CheckState.Unchecked:
            return False

        for child in self.childItems:
            if child.checkState(0) == QtCore.Qt.CheckState.Checked:
                return True
        else:
            return False

    def updateContext(self):
        nodes = list()
        for child in self.childItems:
            if child.checkState(0) == QtCore.Qt.CheckState.Unchecked:
                continue
            nodes.append(child.node)
        self.context["nodes"] = nodes
        self.context["filepath"] = self.filepath

    def setThreading(self, thread):
        self.thread = thread

    def hasThreading(self):
        return self.thread

    def setDisplay(self, progress):
        if progress == 0:
            qcolor = QtGui.QColor(255, 0, 0)
            lable = "Read error, %s" % self.filepath
            self.isRead = False

        if progress == 1:
            qcolor = QtGui.QColor(85, 170, 255)
            lable = "Reading file, %s" % self.filepath
            self.isRead = None

        if progress == 2:
            qcolor = QtGui.QColor(0, 170, 0)
            lable = self.filepath
            self.isRead = True

        if progress == 3:
            qcolor = QtGui.QColor(255, 170, 0)
            lable = "File caching, %s" % self.filepath
            self.isCached = None

        if progress == 4:
            qcolor = QtGui.QColor(255, 0, 0)
            lable = "Caching error, %s" % self.filepath
            self.isCached = False

        if progress == 5:
            qcolor = QtGui.QColor(85, 85, 255)
            lable = self.filepath
            self.isCached = True

        self.setText(0, lable)

        brush = QtGui.QBrush(qcolor)
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.setForeground(0, brush)


class NodeWidgetItem(NormalWidgetItem):
    fontsize = 9
    bold = True

    def __init__(self, parent, *args, **kwargs):
        super(NodeWidgetItem, self).__init__(parent, *args, **kwargs)

        self.name = args[0]
        self.node = args[1]

        self.setText(0, self.node)

    def hasChild(self):
        return True

    def hasSourceItem(self):
        return False


if __name__ == "__main__":
    pass
