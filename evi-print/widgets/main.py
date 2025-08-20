# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)  Resolver QGroupBox wrapper source code.
# WARNING! All changes made in this file will be lost when recompiling UI file!

from __future__ import absolute_import

import widgets
import resources

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import utils
from kore import media
from kore import layers
from kore import logger
from kore import constants

from widgets.menu import FileMenu
from widgets.menu import EditMenu
from widgets.menu import HelpMenu

from widgets.groups import NormalPageGroup
from widgets.groups import InputGroup
from widgets.groups import FieldGroup
from widgets.groups import RenderGroup
from widgets.groups import BarcodeGroup
from widgets.groups import DiagramGroup

# from widgets.groups import BarcodeGroup
from widgets.buttons import TitleButton
from widgets.labels import CopyrightLabel
from widgets.messagebox import DisplayBox
from widgets.groups import TemplateHeaderGroup
from widgets.treewidgets import OutlineTreewidget


LOGGER = logger.getLogger(__name__)
#


class Widget(QtWidgets.QMainWindow):
    def __init__(self, parent=None, **kwargs):
        super(Widget, self).__init__(parent)

        self.name = "evi"
        self.title = kwargs.get("title") or "Launcher 0.0.1"
        self.wsize = kwargs.get("wsize") or [1000, 1000]
        self.titleSize = kwargs.get("titleSize") or [660, 100]
        self.maximize = kwargs.get("maximize")

        self.font = 12
        self.theme = kwargs.get("theme") or "light"
        self.isModified = True
        self.currentIndex = 0

        self.setObjectName("toolBox")

        self.backgroundLayer = layers.BackgroundLayer()
        self.foregroundLayer = layers.ForegroundLayer()
        self.barcodeLayer = layers.BarcodeLayer()

        self.composite = media.Composite()
        self.composite.addBackgroundLayer(self.backgroundLayer)
        self.composite.addForegroundLayer(self.foregroundLayer)
        self.composite.addBarcodeLayer(self.barcodeLayer)

        self.thumbnailContext = resources.getThumbnailPresets()
        self.fieldContext = resources.getFontContext()

        self.templatePath = resources.getTemplatePath()
        self.imagesPath = resources.getTemplatePath()

        self.currentOutlineItem = None
        self.hasLoadedOutlineItems = False

        self.setupUi()
        self.setupIcons()

    def setupUi(self):
        """Gui widgets layouts"""

        self.resize(self.wsize[0], self.wsize[1])
        self.setWindowTitle(self.title)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        widgets.setFontSize(self, self.font, family="Arial", bold=False)
        widgets.setStylesheet(self, theme=self.theme)

        if self.maximize:
            self.showMaximized()

        self.verticallayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticallayout.setSpacing(20)
        self.verticallayout.setContentsMargins(20, 20, 20, 20)

        self.titleButton = TitleButton(
            self, name="evi-resolve", w=self.titleSize[0], h=self.titleSize[1]
        )
        self.verticallayout.addWidget(self.titleButton)

        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.verticallayout.addWidget(self.splitter)

        self.outlineTreewidget = OutlineTreewidget(self)
        # self.sheetTreewidget.setHidden(True)
        self.splitter.addWidget(self.outlineTreewidget)

        # Diagram 0Group
        self.diagramGroup = DiagramGroup(
            self,
            self.composite,
            title="Diagram",
            x=self.thumbnailContext["size"][0]["width"],
            y=self.thumbnailContext["size"][0]["height"],
        )
        # self.splitter_parameter.addWidget(self.diagramGroup)
        self.splitter.addWidget(self.diagramGroup)

        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)

        self.verticallayout_parameter = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticallayout_parameter.setSpacing(5)
        self.verticallayout_parameter.setContentsMargins(10, 10, 10, 10)

        self.toolbox = QtWidgets.QToolBox(self)
        widgets.setFontSize(self.toolbox, self.font, family="Arial", bold=True)
        self.toolbox.setLineWidth(10)

        # self.inputPage = PageGroup(self.toolBox, title="Input")
        # self.barcodePage = PageGroup(self.toolBox, title="Barcode")
        # self.fieldPage = PageGroup(self.toolBox, title="Fields")
        # self.renderPage = PageGroup(self.toolBox, title="Render Settings")

        # Input Group
        self.inputGroup = InputGroup(
            self.toolbox, self.composite, main=self, title="Input", context=self.thumbnailContext
        )
        self.barcodeGroup = BarcodeGroup(self.toolbox, self.composite, main=self, title="Barcode")
        self.fieldGroup = FieldGroup(
            self.toolbox, self.composite, main=self, title="Fields", context=self.fieldContext
        )
        self.renderGroup = RenderGroup(
            self.toolbox, self.composite, main=self, title="Render Settings"
        )

        self.toolbox.setCurrentIndex(self.currentIndex)

        self.templateGroup = TemplateHeaderGroup(self, title="Templates")

        self.verticallayout_parameter.addWidget(self.templateGroup)
        self.verticallayout_parameter.addWidget(self.toolbox)

        # self.verticallayout_parameter.addWidget(self.inputGroup)
        # self.verticallayout_parameter.addWidget(self.barcodeGroup)
        # self.verticallayout_parameter.addWidget(self.fieldGroup)
        # self.verticallayout_parameter.addWidget(self.renderGroup)

        # self.thumbnailFieldGroup = ThumbnailFieldsGroup(self, title="Fields")
        # self.thumbnailFieldGroup.setFiledContext(resources.getFieldContext())
        # self.verticallayout_parameter.addWidget(self.thumbnailFieldGroup)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 927, 22))
        self.setMenuBar(self.menubar)

        self.fileMenu = FileMenu(self)
        self.menubar.addAction(self.fileMenu.menuAction())

        self.editMenu = EditMenu(self)
        self.menubar.addAction(self.editMenu.menuAction())

        self.helpMenu = HelpMenu(self)
        self.menubar.addAction(self.helpMenu.menuAction())

        # self.outputGroup = OutputGroup(self, title="Output")
        # self.verticallayout_parameter.addWidget(self.outputGroup)

        self.copyrightLabel = CopyrightLabel(self)
        self.verticallayout.addWidget(self.copyrightLabel)

        self.splitter.setSizes([386, 414, 1232])

    def setupIcons(self):
        widgets.setWidgetIcon(self, resources.getIconFilepath(self.name))

    def _setDiagram(self):
        inputContext = self.inputGroup.getValue()
        fieldContextList = self.fieldGroup.getValue()
        pixmap = self.diagramGroup.layer.setParameters(**inputContext)
        self.diagramGroup.diagramButton.setDiagram(pixmap, locked=True)

    def setBackground(self):
        self.propertyGroup.setBackground(self.diagramGroup)

    def setForeground(self):
        self.propertyGroup.setForeground(self.diagramGroup)

    def setCurrentOutlineItem(self, outlineItem):
        self.currentOutlineItem = outlineItem

    def contextList(self):
        contextList = [
            self.templateGroup.templateCombobox.context,
            self.outlineTreewidget.getPathContext(),
            self.outlineTreewidget.getContextList(),
        ]
        return contextList

    def renderContextList(self):
        backgroundFilepath = self.backgroundLayer.filepath

        contextList = self.outlineTreewidget.getContextList()
        return backgroundFilepath, contextList

    def setContextList(self, templateContext, pathContext, contextList):
        # Load template
        valid, message = self.templateGroup.templateCombobox.loadCurrentContext(
            templateContext["filename"]
        )

        if not valid:
            DisplayBox(self, "Critical", message, ["Close"])
            LOGGER.warning(message)
            return False
        # Set csv file
        self.outlineTreewidget.loadCurrentContext(pathContext, contextList)

        return True

    def clearAll(self):
        self.currentOutlineItem = None
        self.hasLoadedOutlineItems = False
        self.outlineTreewidget.children = list()

        self.outlineTreewidget.clear()
        self.templateGroup.templateCombobox.clearContext()


if __name__ == "__main__":
    import sys

    appn = QtWidgets.QApplication(sys.argv)
    kwargs = {
        "title": "Evi Resolve 0.0.1",
        "wsize": [2300, 1800],
        "titleSize": [660, 100],
        "theme": "dark",
    }
    window = Widget(parent=None, **kwargs)
    window.show()
    sys.exit(appn.exec_())
