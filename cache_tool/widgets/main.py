# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool

from __future__ import absolute_import

import resources

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from kore import constant

from widgets import Font
from widgets import PixmapIcon
from widgets import SetStylesheet
from widgets.menu import ToolbarMenu
from widgets.groups import SuppertPage
from widgets.labels import TitleLabel
from widgets.groups import ProjectGroup
from widgets.labels import CopyrightLabel
from widgets.groups import CachePropertyPage
from widgets.treewidgets import FileTreewidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, **kwargs):
        super(MainWindow, self).__init__(parent)

        self.name = constant.TOOL_NAME
        self.title = "%s [ Version: %s ]" % (constant.TOOL_TITLE, constant.VERSION)
        self.wsize = kwargs.get("wsize") or [1500, 1200]
        self.titleSize = kwargs.get("titleSize") or [660, 100]
        self.theme = kwargs.get("theme") or constant.GUI_THEMES[0]
        self.maximize = kwargs.get("maximize")

        self.font = constant.FONT_SIZE
        self.application = False

        self.priority = QtCore.QThread.HighestPriority

        self.threadReadPool = QtCore.QThreadPool()
        self.threadReadPool.setMaxThreadCount(self.threadReadPool.maxThreadCount())

        self.threadCachePool = QtCore.QThreadPool()
        self.threadCachePool.setMaxThreadCount(self.threadCachePool.maxThreadCount())

        self.setupUi()
        self.setupIcons()

    def setupUi(self):
        """Gui widgets layouts"""

        self.resize(self.wsize[0], self.wsize[1])
        self.setWindowTitle(self.title)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # widgets.setFontSize(self, self.font, family="Arial", bold=False)

        font = Font(self.font, family="Arial", bold=False)
        self.setFont(font)

        SetStylesheet(self, theme=self.theme)

        if self.maximize:
            self.showMaximized()

        self.verticallayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticallayout.setSpacing(5)
        self.verticallayout.setContentsMargins(10, 10, 10, 10)

        self.titleButton = TitleLabel(self, name="cache-title")
        self.verticallayout.addWidget(self.titleButton)

        self.horizontallayout = QtWidgets.QHBoxLayout()
        self.horizontallayout.setSpacing(5)
        self.horizontallayout.setContentsMargins(1, 1, 1, 1)
        self.verticallayout.addLayout(self.horizontallayout)

        self.toolbarMenu = ToolbarMenu(self)
        self.horizontallayout.addWidget(self.toolbarMenu)

        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.verticallayout.addWidget(self.splitter)

        self.fileTreewidget = FileTreewidget(self)
        self.splitter.addWidget(self.fileTreewidget)

        self.layoutWidget = QtWidgets.QWidget(self)
        self.splitter.addWidget(self.layoutWidget)

        self.verticallayout_panel = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticallayout_panel.setSpacing(5)
        self.verticallayout_panel.setContentsMargins(1, 1, 1, 1)

        self.projectGroup = ProjectGroup(self, title="Project Settings")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        self.projectGroup.setSizePolicy(sizePolicy)
        self.verticallayout_panel.addWidget(self.projectGroup)

        self.toolBox = QtWidgets.QToolBox(self)
        self.verticallayout_panel.addWidget(self.toolBox)

        self.cachePropertyPage = CachePropertyPage(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        self.cachePropertyPage.setProject(self.projectGroup.presetContext["projectPath"])
        self.cachePropertyPage.setSizePolicy(sizePolicy)

        self.toolBox.addItem(self.cachePropertyPage, "Cache Property")
        self.cachePropertyPage.setEnabled(False)

        self.suppertPage = SuppertPage(self)
        self.toolBox.addItem(self.suppertPage, "Support")

        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticallayout.addWidget(self.line)

        self.copyrightLabel = CopyrightLabel(self)
        self.verticallayout.addWidget(self.copyrightLabel)

        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticallayout.addWidget(self.line)

        self.toolBox.setCurrentIndex(1)
        self.splitter.setSizes([917, 548])

    def setupIcons(self):
        icon = PixmapIcon(constant.TOOL_IOCN)
        self.setWindowIcon(icon)


if __name__ == "__main__":
    import sys

    appn = QtWidgets.QApplication(sys.argv)

    kwargs = {
        "wsize": [1500, 1200],
        "titleSize": [1300, 100],
        "maximize": False,
    }
    window = MainWindow(parent=None, **kwargs)
    window.show()
    sys.exit(appn.exec_())
