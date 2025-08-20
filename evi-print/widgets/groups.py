# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)  Resolver QGroupBox wrapper source code.
# WARNING! All changes made in this file will be lost when recompiling UI file!


from __future__ import absolute_import

import widgets
import resources

from functools import partial

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import utils
from kore import media
from kore import stacks
from kore import logger
from kore import layers
from kore import constants

from widgets.labels import NormalVLine
from widgets.labels import NormalHLine

from widgets.labels import ZoomLabel
from widgets.labels import NormalLabel
from widgets.labels import NormalSlider
from widgets.buttons import AddButton
from widgets.buttons import ResetButton
from widgets.buttons import DeleteButton
from widgets.buttons import DiagramButton
from widgets.labels import NormalLineEdit
from widgets.messagebox import DisplayBox

from widgets.buttons import ExportButton
from widgets.buttons import CenterAlignButtons

from widgets.spinboxs import NormalSpinBox
from widgets.buttons import BrowseFileButton
from widgets.spinboxs import NormalDoubleSpinBox
from widgets.comboboxs import TemplateComboBox
from widgets.comboboxs import RenderPageComboBox
from widgets.comboboxs import RenderFormatComboBox
from widgets.buttons import RenderButton
from widgets.buttons import BrowsePathButton
from widgets.labels import PrefixNameLineEdit

from widgets.inputs import InputField
from widgets.inputs import InputSizeWidgets
from widgets.inputs import InputPropertyWidgets
from widgets.labels import NormalProgressBar

from widgets.buttons import CenterAlignButtons
from widgets.buttons import MiddleAlignButtons


from widgets.labels import NormalCheckbox

LOGGER = logger.getLogger(__name__)


class NormalGroup(QtWidgets.QGroupBox):
    def __init__(self, parent, title=None, **kwargs):
        super(NormalGroup, self).__init__(parent, title=title)
        self.__parent__ = parent
        self.title = title

        if self.title:
            self.setTitle(self.title)

        self.setFlat(True)

        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        self.setSizePolicy(sizepolicy)


class NormalPageGroup(QtWidgets.QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(NormalPageGroup, self).__init__(parent)
        self.__parent__ = parent

        self.title = kwargs.get("title")

        parent.addItem(self, self.title)


class TemplateHeaderGroup(NormalGroup):
    def __init__(self, parent, title=None, **kwargs):
        super(TemplateHeaderGroup, self).__init__(parent, title=title)

        self.__parent__ = parent

        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        self.setSizePolicy(sizepolicy)

        self.horizontallayout = QtWidgets.QHBoxLayout(self)
        self.horizontallayout.setSpacing(5)
        self.horizontallayout.setContentsMargins(80, 20, 20, 20)

        self.templateLabel = NormalLabel(
            self,
            label="Current Template",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
            # minimumSize=400,
        )
        widgets.setFontSize(self.templateLabel, self.__parent__.font, family="Arial", bold=False)
        self.horizontallayout.addWidget(self.templateLabel)

        self.templateCombobox = TemplateComboBox(
            self, toolTip="Template", minimumSize=800, templatePath=self.__parent__.templatePath
        )
        self.templateCombobox.loadAllTemplates()
        widgets.setFontSize(self.templateCombobox, self.__parent__.font, family="Arial", bold=False)
        self.horizontallayout.addWidget(self.templateCombobox)

        self.exportButton = ExportButton(self)
        self.exportButton.clicked.connect(self.exportTemplate)
        self.horizontallayout.addWidget(self.exportButton)

        self.horizontalspacer = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontallayout.addItem(self.horizontalspacer)

    def exportTemplate(self):
        filename, ok = QtWidgets.QInputDialog.getText(
            self, "Template Export", "Enter the template name:", QtWidgets.QLineEdit.Normal
        )

        if not ok:
            LOGGER.warning("Export template skipped.")
            return

        bgFilepath = self.__parent__.inputGroup.backgroundLineedit.value()
        fgFilepath = self.__parent__.inputGroup.foregroundLineedit.value()

        bgFilename = "%s-%s%s" % (filename, constants.BACKGROUND, utils.fileExtenstion(bgFilepath))
        fgFilename = "%s-%s%s" % (filename, constants.FOREGROUND, utils.fileExtenstion(fgFilepath))

        bgValid = utils.copyFile(
            bgFilepath, utils.pathResolver(self.__parent__.templatePath, filename=bgFilename)
        )
        fgValid = utils.copyFile(
            fgFilepath, utils.pathResolver(self.__parent__.templatePath, filename=fgFilename)
        )

        valid, message = (
            (False, "Failed?...") if False in [bgValid, fgValid] else (True, "Succeed!...")
        )

        if valid:
            inputContext = self.__parent__.inputGroup.value()
            inputContext["background"] = {"default": bgFilename}
            inputContext["foreground"] = {"default": fgFilename}

            fieldContextList = self.__parent__.fieldGroup.value()
            barcodeContext = self.__parent__.barcodeGroup.value()

            filepath = utils.pathResolver(
                self.__parent__.templatePath, filename="%s.xml" % filename
            )

            valid, message = utils.exportTemplate(
                filepath, inputContext, barcodeContext, fieldContextList
            )

        display = "Information" if valid else "Warning"

        DisplayBox(self, display, message, ["Close"])

        if valid:
            LOGGER.info(message)
        else:
            LOGGER.warning(message)


class DiagramGroup(NormalGroup):
    def __init__(self, parent, composite, title=None, **kwargs):
        super(DiagramGroup, self).__init__(parent, title=title)

        self.composite = composite

        self.y = kwargs.get("y") or 6.4
        self.x = kwargs.get("x") or 4.0

        self.__parent__ = parent

        self.verticallayout = QtWidgets.QVBoxLayout(self)
        self.verticallayout.setSpacing(10)
        self.verticallayout.setContentsMargins(10, 10, 10, 10)

        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout.setVerticalSpacing(10)
        self.gridlayout.setHorizontalSpacing(10)
        self.gridlayout.setContentsMargins(10, 10, 10, 10)
        self.verticallayout.addLayout(self.gridlayout)

        # Height
        self.verticallayout_side = QtWidgets.QVBoxLayout()
        self.verticallayout_side.setSpacing(10)
        self.verticallayout_side.setContentsMargins(10, 10, 10, 10)
        self.gridlayout.addLayout(self.verticallayout_side, 0, 0, 1, 1)

        self.yUpFrame = NormalVLine(self)
        self.verticallayout_side.addWidget(self.yUpFrame)

        self.yLabel = NormalLabel(
            self,
            label=str(self.y),
            alignment="center",
            horizontalPolicy=QtWidgets.QSizePolicy.Fixed,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        self.verticallayout_side.addWidget(self.yLabel)

        self.yDownFrame = NormalVLine(self)
        self.verticallayout_side.addWidget(self.yDownFrame)

        # Width
        self.horizontallayout_down = QtWidgets.QHBoxLayout()
        self.horizontallayout_down.setSpacing(10)
        self.horizontallayout_down.setContentsMargins(10, 10, 10, 10)
        self.gridlayout.addLayout(self.horizontallayout_down, 1, 1, 1, 1)

        self.xLeftFrame = NormalHLine(self)
        self.horizontallayout_down.addWidget(self.xLeftFrame)

        self.xLabel = NormalLabel(
            self,
            label=str(self.x),
            alignment="center",
            horizontalPolicy=QtWidgets.QSizePolicy.Fixed,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        self.horizontallayout_down.addWidget(self.xLabel)

        self.xRightFrame = NormalHLine(self)
        self.horizontallayout_down.addWidget(self.xRightFrame)

        # thumbnailButton
        self.diagramButton = DiagramButton(self)

        # Set default background image
        imageContext = {"background": self.diagramButton.iconpath}
        self.__parent__.backgroundLayer.setContext(**imageContext)
        self.__parent__.backgroundLayer.setActive(True)
        self.defaultPixmap = self.composite.setParameters()

        self.diagramButton.setDiagram(self.defaultPixmap, locked=True)
        self.setLabelSize(
            self.__parent__.backgroundLayer.widthInInches,
            self.__parent__.backgroundLayer.heightInInches,
        )

        self.gridlayout.addWidget(self.diagramButton, 0, 1, 1, 1)

        # Global Scale
        self.horizontallayout_scale = QtWidgets.QHBoxLayout()
        self.verticallayout.addLayout(self.horizontallayout_scale)

        self.scaleLabel = ZoomLabel(self, value=100)
        self.horizontallayout_scale.addWidget(self.scaleLabel)

        self.zoomSlider = NormalSlider(
            self, "Zoom", defaultValue=100, minimum=0, maximum=200, pageStep=1
        )
        self.zoomSlider.valueChanged.connect(self.setZoom)
        self.horizontallayout_scale.addWidget(self.zoomSlider)

        self.zoomResetButton = ResetButton(self)
        self.zoomResetButton.clicked.connect(partial(self.resetWidegtValue, self.zoomSlider))
        self.horizontallayout_scale.addWidget(self.zoomResetButton)

        # self.verticalspacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.gridlayout.addItem(self.verticalspacer, 3, 1, 1, 1)

    def setLabelSize(self, width, height):
        self.xLabel.setValue(str(width))
        self.yLabel.setValue(str(height))

    def setValues(self, context):
        self.xLabel.setValue(str(context.get("x")))
        self.yLabel.setValue(str(context.get("y")))

    def setZoom(self, index):
        self.diagramButton.setDisplay((index - 100) * 4, locked=True)
        self.scaleLabel.setValue(index)

    def resetWidegtValue(self, widget):
        widget.setValues()


class InputGroup(NormalPageGroup):
    def __init__(self, parent, composite, **kwargs):
        super(InputGroup, self).__init__(parent, composite, **kwargs)

        self.__parent__ = kwargs.get("main")
        self.composite = composite
        self.context = kwargs.get("context")

        self.inputContext = dict()  # for load csv file

        self.pause = False

        # self.backgroundLayer = layers.BackgroundLayer()
        # self.composite.addBackgroundLayer(self.backgroundLayer)
        # self.foregroundLayer = layers.ForegroundLayer()
        # self.composite.addForegroundLayer(self.foregroundLayer)

        self.setMinimumSize(QtCore.QSize(400, 0))
        # self.setMaximumSize(QtCore.QSize(400, 16777215))

        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        self.setSizePolicy(sizepolicy)

        self.gridlayout = QtWidgets.QGridLayout(self)
        self.gridlayout.setVerticalSpacing(10)
        self.gridlayout.setHorizontalSpacing(10)
        self.gridlayout.setContentsMargins(20, 20, 20, 20)

        self.sizeLabel = NormalLabel(
            self,
            label="Size",
            alignment="right",
            maximumSize=150,
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        self.gridlayout.addWidget(self.sizeLabel, 0, 0, 1, 1)

        self.horizontallayout = QtWidgets.QHBoxLayout()
        self.horizontallayout.setSpacing(10)
        self.horizontallayout.setContentsMargins(10, 10, 10, 10)
        self.gridlayout.addLayout(self.horizontallayout, 0, 1, 1, 1)

        # Size columns
        self.inputSizeWidgets = InputSizeWidgets(self, self.context["size"], self.horizontallayout)
        # self.inputSizeWidgets.setValue(backgroundLayer=self.__parent__.diagramGroup.backgroundLayer)

        # background image columns
        self.backgroundLabel = NormalLabel(
            self,
            label="Backgroud",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        self.gridlayout.addWidget(self.backgroundLabel, 2, 0, 1, 1)

        self.backgroundLineedit = NormalLineEdit(self, defaultValue=None)

        # Signal connections
        self.backgroundLineedit.textChanged.connect(self.setBackground)
        # self.backgroundLineedit.editingFinished.connect(self.setBackground)

        self.gridlayout.addWidget(self.backgroundLineedit, 2, 1, 1, 4)

        self.backgroundBrowseButton = BrowseFileButton(
            self, widget=self.backgroundLineedit, formats=constants.IMAGE_EXTENSTIONS
        )
        self.gridlayout.addWidget(self.backgroundBrowseButton, 2, 5, 1, 1)

        self.backgroundResetButton = ResetButton(self)
        self.backgroundResetButton.clicked.connect(
            partial(self.resetWidegtValue, self.backgroundLineedit)
        )
        self.gridlayout.addWidget(self.backgroundResetButton, 2, 6, 1, 1)

        # Foreground image columns
        self.foregroundLabel = NormalLabel(
            self,
            label="Forground",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        self.gridlayout.addWidget(self.foregroundLabel, 3, 0, 1, 1)

        self.foregroundLineedit = NormalLineEdit(self)

        # Signal connections
        self.foregroundLineedit.textChanged.connect(self.setForeground)
        # self.foregroundLineedit.editingFinished.connect(self.setForeground)

        self.gridlayout.addWidget(self.foregroundLineedit, 3, 1, 1, 4)

        self.foregroundBrowseButton = BrowseFileButton(
            self, widget=self.foregroundLineedit, formats=["png", "jpg", "jpeg", "tga"]
        )
        self.gridlayout.addWidget(self.foregroundBrowseButton, 3, 5, 1, 1)

        self.foregroundResetButton = ResetButton(self)
        self.foregroundResetButton.clicked.connect(
            partial(self.resetWidegtValue, self.foregroundLineedit)
        )
        self.gridlayout.addWidget(self.foregroundResetButton, 3, 6, 1, 1)

        # Foreground property layout columns
        self.gridlayout_foreground = QtWidgets.QGridLayout()
        self.gridlayout_foreground.setVerticalSpacing(10)
        self.gridlayout_foreground.setHorizontalSpacing(10)
        self.gridlayout_foreground.setContentsMargins(10, 10, 10, 10)
        self.gridlayout.addLayout(self.gridlayout_foreground, 4, 1, 1, 6)

        self.inputProperties = InputPropertyWidgets(self, self.gridlayout_foreground)

    def setBackground(self):
        if self.pause:
            return

        filepath = self.backgroundLineedit.value() or None

        if filepath is not None and not utils.hasFileExists(filepath):
            DisplayBox(self, "Warning", "Invalid source background file path", ["Close"])
            LOGGER.warning("Invalid source background file path")
            return

        imageContext = self.getValue()
        self.__parent__.backgroundLayer.setContext(**imageContext)

        pixmap = self.composite.setParameters()

        self.__parent__.diagramGroup.diagramButton.setDiagram(pixmap, locked=True)
        self.__parent__.diagramGroup.setLabelSize(
            self.__parent__.backgroundLayer.widthInInches,
            self.__parent__.backgroundLayer.heightInInches,
        )

        self.inputSizeWidgets.setValue(backgroundLayer=self.__parent__.backgroundLayer)

    def setForeground(self):
        if self.pause:
            return

        filepath = self.foregroundLineedit.value() or None

        if filepath is not None and not utils.hasFileExists(filepath):
            DisplayBox(self, "Warning", "Invalid source foreground file path", ["Close"])
            LOGGER.warning("Invalid source foreground file path, ( %s )" % filepath)
            return

        if not filepath:
            return

        imageContext = self.getValue()

        self.__parent__.foregroundLayer.setContext(**imageContext)
        self.__parent__.foregroundLayer.setActive(True)

        pixmap = self.composite.setParameters()

        self.__parent__.diagramGroup.diagramButton.setDiagram(pixmap, locked=True)

        self.inputProperties.setDefaultValues()

    def getValue(self):
        backgroundFilepath = self.backgroundLineedit.value()

        if not backgroundFilepath:
            backgroundFilepath = self.__parent__.diagramGroup.diagramButton.iconpath

        context = {
            "background": backgroundFilepath,
            "foreground": self.foregroundLineedit.value(),
        }
        # context.update(self.inputSizeWidgets.getValue())
        # context.update(self.inputProperties.getValue())
        return context

    def setValues(self, context):
        # backgroundFilepath = utils.pathResolver(self.__parent__.templatePath, filename=context["background"]["default"])

        self.inputContext = context

        backgroundFilepath = context["background"]["default"]
        foregroundFilepath = context["foreground"]["default"]

        with stacks.Pause(self):
            self.backgroundLineedit.setValue(backgroundFilepath)
            self.foregroundLineedit.setValue(foregroundFilepath)

        logger.nextLine()
        LOGGER.info("Background filepath, %s" % backgroundFilepath)
        LOGGER.info("Foreground filepath, %s" % foregroundFilepath)

        self.setBackground()
        self.setForeground()

        values = [
            context["x"]["value"] if "value" in context["x"] else context["x"]["default"],
            context["y"]["value"] if "value" in context["y"] else context["y"]["default"],
            context["scale"]["value"]
            if "value" in context["scale"]
            else context["scale"]["default"],
            context["mask"]["value"] if "value" in context["mask"] else context["mask"]["default"],
            context["shape"]["value"]
            if "value" in context["shape"]
            else context["shape"]["default"],
            context["stroke"]["value"]
            if "value" in context["stroke"]
            else context["stroke"]["default"],
            context["color"]["value"]
            if "value" in context["color"]
            else context["color"]["default"],
        ]

        self.inputProperties.setValue(*values)
        self.inputProperties.setDiagram()

        # layer = self.__parent__.diagramGroup.layer
        # layer.setBackground(backgroundFilepath)
        # layer.setForeground(foregroundFilepath)

        # self.inputSizeWidgets.setValue(backgroundLayer=layer.backgroundLayer)
        # self.inputProperties.setDefaultValues()

        return

    def resetWidegtValue(self, widget):
        widget.setValues()
        # LOGGER.info("Set the background image to, %s" % filepath)

    def _setInputContext(self, context):
        self.inputContext = context

    def _setForeground(self, value):
        if self.pause:
            return

        filepath = self.foregroundLineedit.value() or None

        if filepath is not None and not utils.hasFileExists(filepath):
            DisplayBox(self, "Warning", "Invalid source foreground file path", ["Close"])
            LOGGER.warning("Invalid source foreground file path, ( %s )" % filepath)
            return

        if not filepath:
            return

        pixmap = self.__parent__.diagramGroup.layer.setForeground(filepath)

        self.inputProperties.setDefaultValues()

        self.inputProperties.setDiagram()

        return

        for inputField in self.__parent__.fieldGroup.children:
            inputField.setDefaultValues()

        if not self.pause:
            with stacks.Pause(self):
                # self.__parent__.diagramGroup.diagramButton.setDiagram(pixmap, locked=True)
                self.inputProperties.setDiagram()

    def value(self):
        context = {
            "resolution": {"default": self.inputSizeWidgets.resolutionSpinbox.value()},
            # "inputSize":  self.inputSizeWidgets.value(),
            "background": {"default": self.backgroundLineedit.value()},
            "foreground": {"default": self.foregroundLineedit.value()},
            # "properties": self.inputProperties.value()
        }
        context.update(self.inputSizeWidgets.value())
        context.update(self.inputProperties.value())
        return context

    def _getValue(self):
        context = {
            "resolution": self.inputSizeWidgets.resolutionSpinbox.value(),
            "background": self.backgroundLineedit.value(),
            "foreground": self.foregroundLineedit.value(),
        }
        context.update(self.inputSizeWidgets.getValue())
        context.update(self.inputProperties.getValue())
        return context

    def _setChildWidgetItemContext(self, index, context):
        self.childWidgetItemContext[index] = context

    def clear(self):
        self.backgroundLineedit.clear()
        self.foregroundLineedit.clear()
        self.inputProperties.clear()


class BarcodeGroup(NormalPageGroup):
    def __init__(self, parent, composite, **kwargs):
        super(BarcodeGroup, self).__init__(parent, composite, **kwargs)

        self.__parent__ = kwargs.get("main")
        self.composite = composite

        # print(self.__parent__.barcodeLayer)

        self.composite = composite

        self.pause = False
        self.checked = False

        self.barcodeContext = dict()  # for load csv file

        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        self.setSizePolicy(sizepolicy)

        self.gridlayout = QtWidgets.QGridLayout(self)
        self.gridlayout.setVerticalSpacing(20)
        self.gridlayout.setHorizontalSpacing(20)
        self.gridlayout.setContentsMargins(20, 30, 20, 20)

        self.fieldCheckbox = NormalCheckbox(
            self,
            label="Field",
            value=self.checked,
            alignment="right",
            minimumSize=150,
            horizontalPolicy=QtWidgets.QSizePolicy.Fixed,
            veritcalPolicy=QtWidgets.QSizePolicy.Preferred,
        )
        self.fieldCheckbox.stateChanged.connect(self.setBarcodeEnable)
        self.gridlayout.addWidget(self.fieldCheckbox, 0, 0, 1, 1)

        self.fieldLineEdit = NormalLineEdit(
            self,
            label="barcode",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        self.fieldLineEdit.setEnabled(False)
        self.gridlayout.addWidget(self.fieldLineEdit, 0, 1, 1, 1)

        self.valueLabel = NormalLabel(
            self,
            label="Value",
            alignment="right",
            minimumSize=80,
            horizontalPolicy=QtWidgets.QSizePolicy.Fixed,
            veritcalPolicy=QtWidgets.QSizePolicy.Preferred,
        )
        self.gridlayout.addWidget(self.valueLabel, 0, 2, 1, 1)

        self.valueLineEdit = NormalLineEdit(
            self,
            label=None,
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        self.valueLineEdit.editingFinished.connect(self.setBarcode)
        self.gridlayout.addWidget(self.valueLineEdit, 0, 3, 1, 1)

        # self.horizontalspacer = QtWidgets.QSpacerItem(458, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.gridlayout.addItem(self.horizontalspacer, 0, 4, 1, 2)

        self.horizontallayout_align = QtWidgets.QHBoxLayout()
        self.horizontallayout_align.setSpacing(10)
        self.horizontallayout_align.setContentsMargins(10, 10, 10, 10)
        self.gridlayout.addLayout(self.horizontallayout_align, 0, 4, 1, 2)

        self.centerAlignButtons = CenterAlignButtons(
            self.__parent__, self.horizontallayout_align, align="center"
        )

        self.horizontalSpacer_center = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontallayout_align.addItem(self.horizontalSpacer_center)

        self.middleAlignButtons = MiddleAlignButtons(
            self.__parent__, self.horizontallayout_align, align="middle"
        )

        self.horizontalSpacer_middle = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontallayout_align.addItem(self.horizontalSpacer_middle)

        self.positionXLabel = NormalLabel(
            self,
            label="Position: X",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )

        self.gridlayout.addWidget(self.positionXLabel, 1, 0, 1, 1)

        self.positionXSpinbox = NormalSpinBox(
            self,
            toolTip="Barcode position X parameter",
            minimum=0,
            maximum=100,
            step=1,
            symbols=QtWidgets.QAbstractSpinBox.PlusMinus,
            defaultValue=0,
            minimumSize=150,
            maximumSize=150,
        )
        self.gridlayout.addWidget(self.positionXSpinbox, 1, 1, 1, 1)

        self.positionXSlider = NormalSlider(
            self,
            "x",
            defaultValue=0.0,
            minimum=1,
            maximum=100,
            spinebox=self.positionXSpinbox,
        )
        self.positionXSlider.valueChanged.connect(
            partial(self.setValueChange, self.positionXSpinbox)
        )
        self.positionXSpinbox.valueChanged.connect(
            partial(self.setIndexChange, self.positionXSlider)
        )
        self.gridlayout.addWidget(self.positionXSlider, 1, 2, 1, 3)

        self.positionXResetButton = ResetButton(self)
        self.positionXResetButton.clicked.connect(
            partial(self.resetWidegtValue, self.positionXSlider)
        )
        self.gridlayout.addWidget(self.positionXResetButton, 1, 5, 1, 1)

        self.positionYLabel = NormalLabel(
            self,
            label="Y",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        self.gridlayout.addWidget(self.positionYLabel, 2, 0, 1, 1)

        self.positionYSpinbox = NormalSpinBox(
            self,
            toolTip="Barcode position Y parameter",
            minimum=0,
            maximum=100,
            step=1,
            symbols=QtWidgets.QAbstractSpinBox.PlusMinus,
            defaultValue=0,
            minimumSize=150,
            maximumSize=150,
        )
        self.gridlayout.addWidget(self.positionYSpinbox, 2, 1, 1, 1)

        self.positionYSlider = NormalSlider(
            self,
            "y",
            defaultValue=0.0,
            minimum=1,
            # maximum=100,
            spinebox=self.positionYSpinbox,
        )
        self.positionYSlider.valueChanged.connect(
            partial(self.setValueChange, self.positionYSpinbox)
        )
        self.positionYSpinbox.valueChanged.connect(
            partial(self.setIndexChange, self.positionYSlider)
        )
        self.gridlayout.addWidget(self.positionYSlider, 2, 2, 1, 3)

        self.positionYResetButton = ResetButton(self)
        self.positionYResetButton.clicked.connect(
            partial(self.resetWidegtValue, self.positionYSlider)
        )
        self.gridlayout.addWidget(self.positionYResetButton, 2, 5, 1, 1)

        self.centerAlignButtons.leftButton.clicked.connect(
            partial(self.setAlignment, self.positionXSlider, "left")
        )
        self.centerAlignButtons.centerButton.clicked.connect(
            partial(self.setAlignment, self.positionXSlider, "center")
        )
        self.centerAlignButtons.rightButton.clicked.connect(
            partial(self.setAlignment, self.positionXSlider, "right")
        )

        self.middleAlignButtons.topButton.clicked.connect(
            partial(self.setAlignment, self.positionYSlider, "top")
        )
        self.middleAlignButtons.middleButton.clicked.connect(
            partial(self.setAlignment, self.positionYSlider, "middle")
        )
        self.middleAlignButtons.bottomButton.clicked.connect(
            partial(self.setAlignment, self.positionYSlider, "bottom")
        )

        self.scaleLabel = NormalLabel(
            self,
            label="Scale",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        self.gridlayout.addWidget(self.scaleLabel, 3, 0, 1, 1)

        self.scaleSpinbox = NormalSpinBox(
            self,
            toolTip="Barcode scale parameter",
            minimum=0,
            maximum=200,
            step=1,
            symbols=QtWidgets.QAbstractSpinBox.PlusMinus,
            defaultValue=100,
            minimumSize=150,
            maximumSize=100,
        )
        self.gridlayout.addWidget(self.scaleSpinbox, 3, 1, 1, 1)

        self.scaleSlider = NormalSlider(
            self,
            "scale",
            defaultValue=100,
            minimum=0,
            maximum=200,
            spinebox=self.scaleSpinbox,
        )
        self.scaleSlider.valueChanged.connect(partial(self.setValueChange, self.scaleSpinbox))
        self.scaleSpinbox.valueChanged.connect(partial(self.setIndexChange, self.scaleSlider))
        self.gridlayout.addWidget(self.scaleSlider, 3, 2, 1, 3)

        self.scaleResetButton = ResetButton(self)
        self.scaleResetButton.clicked.connect(partial(self.resetWidegtValue, self.scaleSlider))
        self.gridlayout.addWidget(self.scaleResetButton, 3, 5, 1, 1)

        self.setBarcodeEnable(self.checked)

    def resetWidegtValue(self, widget):
        widget.setValues()

    def setBarcodeEnable(self, checked):
        self.checked = bool(checked)

        self.valueLineEdit.clear()
        self.positionXSpinbox.setValue(0)
        self.positionXSlider.setValue(0)
        self.positionYSpinbox.setValue(0)
        self.positionYSlider.setValue(0)
        self.scaleSpinbox.setValue(100)
        self.scaleSlider.setValue(100)

        self.fieldLineEdit.setVisible(self.checked)
        self.valueLabel.setVisible(self.checked)
        self.valueLineEdit.setVisible(self.checked)

        self.positionXLabel.setVisible(self.checked)
        self.positionXSpinbox.setVisible(self.checked)
        self.positionXSlider.setVisible(self.checked)
        self.positionXResetButton.setVisible(self.checked)

        self.positionYLabel.setVisible(self.checked)
        self.positionYSpinbox.setVisible(self.checked)
        self.positionYSlider.setVisible(self.checked)
        self.positionYResetButton.setVisible(self.checked)
        self.scaleLabel.setVisible(self.checked)
        self.scaleSpinbox.setVisible(self.checked)
        self.scaleSlider.setVisible(self.checked)
        self.scaleResetButton.setVisible(self.checked)

        self.centerAlignButtons.setVisible(self.checked)
        self.middleAlignButtons.setVisible(self.checked)

        if not checked:
            self.__parent__.barcodeLayer.setActive(False)
            self.setDiagram()

    def _setBarcodeContext(self, context):
        self.barcodeContext = context

    def setDefaultValues(self):
        alignments = self.__parent__.barcodeLayer.getAlignments()
        positionRange = self.__parent__.barcodeLayer.getPositionRange()

        with stacks.Pause(self):
            self.positionXSpinbox.setLimits(positionRange["x"][0], positionRange["x"][1])
            self.positionXSlider.setLimits(positionRange["x"][0], positionRange["x"][1])

            self.positionYSpinbox.setLimits(positionRange["y"][0], positionRange["y"][1])
            self.positionYSlider.setLimits(positionRange["y"][0], positionRange["y"][1])

            self.positionXSpinbox.setDefaultValue(alignments["center"]["x"])
            self.positionYSpinbox.setDefaultValue(alignments["middle"]["y"])

            self.positionXSlider.setDefaultValue(alignments["center"]["x"])
            self.positionYSlider.setDefaultValue(alignments["middle"]["y"])

            # self.positionXSlider.setValue(alignments["center"]["x"])
            # self.positionYSlider.setValue(alignments["middle"]["y"])

            # self.positionXSpinbox.setValue(alignments["center"]["x"])
            # self.positionYSpinbox.setValue(alignments["middle"]["y"])

    def setBarcode(self, *args):
        if self.pause:
            return

        self.setDiagram()
        self.setDefaultValues()

    def setValueChange(self, widget, value):
        if self.pause:
            return
        widget.setValue(value)

    def setIndexChange(self, widget, index):
        with stacks.Pause(self):
            widget.setValue(index)
            self.setDiagram()

    def setValues(self, context):
        if not context.get("checked"):
            self.fieldCheckbox.setChecked(False)
            return

        self.barcodeContext = context

        values = [
            context["checked"]["value"]
            if "value" in context["checked"]
            else context["checked"]["default"],
            context["text"]["value"] if "value" in context["text"] else context["text"]["default"],
            context["x"]["value"] if "value" in context["x"] else context["x"]["default"],
            context["y"]["value"] if "value" in context["y"] else context["y"]["default"],
            context["scale"]["value"]
            if "value" in context["scale"]
            else context["scale"]["default"],
        ]

        with stacks.Pause(self):
            self.setValue(*values)

        self.setDiagram()
        self.setDefaultValues()

    def setValue(self, checked, text, x, y, scale):
        self.fieldCheckbox.setChecked(checked)
        self.valueLineEdit.setValue(text)
        self.positionXSpinbox.setValue(x)
        self.positionYSpinbox.setValue(y)
        self.scaleSpinbox.setValue(scale)

    def getValue(self):
        textLayerContext = {
            "text": self.valueLineEdit.value(),
            "x": self.positionXSpinbox.value(),
            "y": self.positionYSpinbox.value(),
            "scale": self.scaleSpinbox.value(),
            "format": "PNG",
            "fontSize": 7,
            "textDistance": 3,
            "quietZone": 6.5,
            "dpi": self.__parent__.backgroundLayer.resolution or 300,
            "background": "white",
            "foreground": "black",
        }
        return textLayerContext

    def setDiagram(self):  # Final #######################
        barcodeContext = self.getValue()
        self.__parent__.barcodeLayer.setContext(**barcodeContext)
        self.__parent__.barcodeLayer.setActive(True)
        pixmap = self.composite.setParameters()
        self.__parent__.diagramGroup.diagramButton.setDiagram(pixmap, locked=True)

        if self.__parent__.currentOutlineItem:
            self.__parent__.currentOutlineItem.setOverrideBarcodeContext(barcodeContext)

    def setAlignment(self, widget, direction):
        barcodeLayer = self.__parent__.barcodeLayer

        if not barcodeLayer or not barcodeLayer.isActive:
            LOGGER.warning("Foreground Layer does not active, load foreground image and try")
            return

        alignments = barcodeLayer.getAlignments()
        positionRange = barcodeLayer.getPositionRange()

        widget.setLimits(positionRange[widget.axis][0], positionRange[widget.axis][1])
        widget.spinebox.setLimits(positionRange[widget.axis][0], positionRange[widget.axis][1])

        widget.setValue(alignments[direction][widget.axis])

    def value(self):
        context = {
            "checked": {"default": self.checked},
            "text": {"default": self.valueLineEdit.value()},
            "x": {"default": self.positionXSpinbox.value()},
            "y": {"default": self.positionYSpinbox.value()},
            "scale": {"default": self.scaleSpinbox.value()},
            "format": {"default": "PNG"},
            "fontSize": {"default": 7},
            "textDistance": {"default": 3},
            "quietZone": {"default": 6.5},
            "dpi": {"default": self.__parent__.backgroundLayer.resolution},
            "background": {"default": "white"},
            "foreground": {"default": "black"},
        }
        return context

    def clear(self):
        self.valueLineEdit.clear()
        # self.positionXSpinbox.setDefault()
        # self.positionXSlider.setDefault()
        # self.positionYSpinbox.setDefault()
        # self.positionYSlider.setDefault()
        # self.scaleSpinbox.setDefault()
        # self.scaleYSlider.setDefault()


class FieldGroup(NormalPageGroup):
    def __init__(self, parent, composite, **kwargs):
        super(FieldGroup, self).__init__(parent, composite, **kwargs)

        self.__parent__ = kwargs.get("main")
        self.composite = composite
        self.context = kwargs.get("context")

        # self.diagramGroup = parent.diagramGroup

        self.fieldContextList = list()

        self.children = list()

        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        self.setSizePolicy(sizepolicy)

        self.verticallayout = QtWidgets.QVBoxLayout(self)
        self.verticallayout.setSpacing(10)
        self.verticallayout.setContentsMargins(10, 30, 10, 10)

        # self.barcodeGroup = BarcodeGroup(self, title="Barcode")
        # self.verticallayout.addWidget(self.barcodeGroup)

        self.scrollarea = QtWidgets.QScrollArea(self)
        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        self.scrollarea.setSizePolicy(sizepolicy)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.verticallayout.addWidget(self.scrollarea)

        self.scrollareawidget = QtWidgets.QWidget()
        self.scrollarea.setWidget(self.scrollareawidget)

        self.verticallayout_scroll = QtWidgets.QVBoxLayout(self.scrollareawidget)
        self.verticallayout_scroll.setSpacing(20)
        self.verticallayout_scroll.setContentsMargins(0, 0, 0, 0)

        # =============================================================================================================================================
        # self.gridlayout = QtWidgets.QGridLayout()
        # self.gridlayout.setVerticalSpacing(20)
        # self.gridlayout.setHorizontalSpacing(20)
        # self.gridlayout.setContentsMargins(10, 10, 10, 10)
        # self.verticallayout_scroll.addLayout(self.gridlayout)
        # =============================================================================================================================================

        self.verticallayout_property = QtWidgets.QVBoxLayout()
        self.verticallayout_property.setSpacing(20)
        self.verticallayout_property.setContentsMargins(10, 10, 10, 10)
        self.verticallayout_scroll.addLayout(self.verticallayout_property)

        self.horizontallayout = QtWidgets.QHBoxLayout()
        self.horizontallayout.setSpacing(20)
        self.horizontallayout.setContentsMargins(10, 10, 10, 10)
        self.verticallayout_scroll.addLayout(self.horizontallayout)

        self.addButton = AddButton(self)
        self.addButton.clicked.connect(partial(self.addNewField, default=True))
        self.horizontallayout.addWidget(self.addButton)

        self.horizontalspacer_add = QtWidgets.QSpacerItem(
            200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontallayout.addItem(self.horizontalspacer_add)

        self.centerAlignButtons = CenterAlignButtons(self, self.horizontallayout, align="left")
        self.centerAlignButtons.leftButton.clicked.connect(self.setAlignment)
        self.centerAlignButtons.centerButton.clicked.connect(self.setAlignment)
        self.centerAlignButtons.rightButton.clicked.connect(self.setAlignment)

        self.horizontalspacer_align = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontallayout.addItem(self.horizontalspacer_align)

    def addNewField(self, default=False):
        # if not self.__parent__.foregroundLayer.isActive:
        #    DisplayBox(self, "Warning", "Load foreground image and try", ["Close"])
        #    return

        index = len(self.children)
        inputField = InputField(self, index, self.verticallayout_property, self.context)
        self.children.append(inputField)

        inputField.setContext()
        # inputField.setDefaultValues()
        # if self.__parent__.diagramGroup.layer.foregroundLayer and default:
        #     inputField.setDefaultValues()

        return inputField

    def setAlignment(self):
        direction = self.centerAlignButtons.value()
        for child in self.children[1:]:
            child.centerAlignButtons.setValue(direction)
            child.setAlignment()

    def value(self):
        contextList = list()

        for child in self.children:
            contexts = [
                {"index": {"default": child.index}},
                {"field": {"default": child.fieldLineEdit.value()}},
                {"text": {"default": child.valueLineEdit.value()}},
                {"size": {"default": child.sizeSpinbox.value()}},
                {"family": {"default": child.fontFamilyCombobox.value()}},
                {"fillColor": {"default": child.colorButton.value()}},
                {"x": {"default": child.positionXSpinbox.value()}},
                {"y": {"default": child.positionYSpinbox.value()}},
                {"stroke": {"default": child.strokeSpinBox.value()}},
                {"strokeColor": {"default": child.strokeColorButton.value()}},
                {"spacing": {"default": child.spaceSpinBox.value()}},
                {"bold": {"default": False}},
                {"italic": {"default": False}},
                {"underline": {"default": False}},
                {"overline": {"default": False}},
                {"strikeOut": {"default": False}},
                {"wordSpacing": {"default": 0}},
                {"stretch": {"default": 0}},
                {"capitalization": {"default": "mixedCase"}},
            ]
            contextList.append(contexts)

        return contextList

    def getValue(self):
        contextList = list()

        for child in self.children:
            contexts = [
                {"index": child.index},
                {"field": child.fieldLineEdit.value()},
                {"text": child.valueLineEdit.value()},
                {"size": child.sizeSpinbox.value()},
                {"family": child.fontFamilyCombobox.value()},
                {"fillColor": child.colorButton.value()},
                {"x": child.positionXSpinbox.value()},
                {"y": child.positionYSpinbox.value()},
                {"stroke": child.strokeSpinBox.value()},
                {"strokeColor": child.strokeColorButton.value()},
                {"spacing": child.spaceSpinBox.value()},
                {"align": child.centerAlignButtons.value()},
                {"bold": False},
                {"italic": False},
                {"underline": False},
                {"overline": False},
                {"strikeOut": False},
                {"wordSpacing": 0},
                {"stretch": 0},
                {"capitalization": "mixedCase"},
            ]
            contextList.append(contexts)

        return contextList

    def setValues(self, contextList):
        self.fieldContextList = contextList
        for context in contextList:
            inputField = self.addNewField()

            values = [
                context["field"]["value"]
                if "value" in context["field"]
                else context["field"]["default"],
                context["text"]["value"]
                if "value" in context["text"]
                else context["text"]["default"],
                context["size"]["value"]
                if "value" in context["size"]
                else context["size"]["default"],
                context["family"]["value"]
                if "value" in context["family"]
                else context["family"]["default"],
                context["fillColor"]["value"]
                if "value" in context["fillColor"]
                else context["fillColor"]["default"],
                context["stroke"]["value"]
                if "value" in context["stroke"]
                else context["stroke"]["default"],
                context["strokeColor"]["value"]
                if "value" in context["strokeColor"]
                else context["strokeColor"]["default"],
                context["spacing"]["value"]
                if "value" in context["spacing"]
                else context["spacing"]["default"],
                context["x"]["value"] if "value" in context["x"] else context["x"]["default"],
                context["y"]["value"] if "value" in context["y"] else context["y"]["default"],
                context["bold"]["value"]
                if "value" in context["bold"]
                else context["bold"]["default"],
                context["italic"]["value"]
                if "value" in context["italic"]
                else context["italic"]["default"],
                context["underline"]["value"]
                if "value" in context["underline"]
                else context["underline"]["default"],
                context["overline"]["value"]
                if "value" in context["overline"]
                else context["overline"]["default"],
                context["strikeOut"]["value"]
                if "value" in context["strikeOut"]
                else context["strikeOut"]["default"],
                context["wordSpacing"]["value"]
                if "value" in context["wordSpacing"]
                else context["wordSpacing"]["default"],
                context["stretch"]["value"]
                if "value" in context["stretch"]
                else context["stretch"]["default"],
                context["capitalization"]["value"]
                if "value" in context["capitalization"]
                else context["capitalization"]["default"],
            ]

            with stacks.Pause(inputField):
                inputField.setValue(*values)

            inputField.fieldLineEdit.setEnabled(False)
            inputField.setDiagram()
            inputField.setDefaultValues()

    def clear(self):
        for child in self.children:
            child.deleteLater()

        self.children = list()

        return


class RenderGroup(NormalPageGroup):
    def __init__(self, parent, composite, **kwargs):
        super(RenderGroup, self).__init__(parent, composite, **kwargs)

        self.__parent__ = kwargs.get("main")
        self.composite = composite

        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        self.setSizePolicy(sizepolicy)

        self.boxChecked = False

        # self.setCheckable(True)
        # self.setChecked(False)

        self.gridlayout = QtWidgets.QGridLayout(self)
        self.gridlayout.setVerticalSpacing(20)
        self.gridlayout.setHorizontalSpacing(20)
        self.gridlayout.setContentsMargins(20, 30, 20, 20)

        self.filepathLabel = NormalLabel(
            self,
            label="Output Directory",
            alignment="right",
            minimumSize=150,
            horizontalPolicy=QtWidgets.QSizePolicy.Fixed,
            veritcalPolicy=QtWidgets.QSizePolicy.Preferred,
        )
        self.gridlayout.addWidget(self.filepathLabel, 0, 0, 1, 1)

        self.filepathLineedit = NormalLineEdit(
            self,
            label=None,
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        self.gridlayout.addWidget(self.filepathLineedit, 0, 1, 1, 2)

        self.browseButton = BrowsePathButton(
            self, widget=self.filepathLineedit, formats=["png", "jpg", "jpeg", "tga"]
        )
        self.gridlayout.addWidget(self.browseButton, 0, 3, 1, 1)

        self.prefixNameLabel = NormalLabel(
            self,
            label="File Name Prefix",
            alignment="right",
            minimumSize=150,
            horizontalPolicy=QtWidgets.QSizePolicy.Fixed,
            veritcalPolicy=QtWidgets.QSizePolicy.Preferred,
        )
        self.gridlayout.addWidget(self.prefixNameLabel, 1, 0, 1, 1)

        self.prefixNameLineedit = PrefixNameLineEdit(
            self,
            label=None,
            minimumSize=400,
            maximumSize=400,
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        self.gridlayout.addWidget(self.prefixNameLineedit, 1, 1, 1, 1)

        self.horizontalspacer = QtWidgets.QSpacerItem(
            52, 19, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridlayout.addItem(self.horizontalspacer, 1, 2, 1, 2)

        self.pageLabel = NormalLabel(
            self,
            label="Page",
            alignment="right",
            minimumSize=150,
            horizontalPolicy=QtWidgets.QSizePolicy.Fixed,
            veritcalPolicy=QtWidgets.QSizePolicy.Preferred,
        )
        # self.pageLabel.setStyleSheet("background-color: rgb(255, 170, 0);")

        self.gridlayout.addWidget(self.pageLabel, 2, 0, 1, 1)

        self.pageCombobox = RenderPageComboBox(self)
        self.gridlayout.addWidget(self.pageCombobox, 2, 1, 1, 1)

        self.formatLabel = NormalLabel(
            self,
            label="Format",
            alignment="right",
            minimumSize=150,
            horizontalPolicy=QtWidgets.QSizePolicy.Fixed,
            veritcalPolicy=QtWidgets.QSizePolicy.Preferred,
        )
        self.gridlayout.addWidget(self.formatLabel, 3, 0, 1, 1)

        self.formatCombobox = RenderFormatComboBox(self)
        self.gridlayout.addWidget(self.formatCombobox, 3, 1, 1, 1)

        self.renderButton = RenderButton(self)
        self.renderButton.clicked.connect(self.startRender)
        self.gridlayout.addWidget(self.renderButton, 4, 1, 1, 1)

        self.renderProgressBar = NormalProgressBar(self)
        self.renderProgressBar.hide()
        self.gridlayout.addWidget(self.renderProgressBar, 5, 1, 1, 1)

        # self.setRenderEnable(self.boxChecked)

        # self.toggled.connect(self.setRenderEnable)
        # checkable, toggled()
        # self.verticalspacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        # self.gridlayout.addItem(self.verticalspacer, 5, 0, 1, 1)

    def setRenderEnable(self, checked):
        self.boxChecked = bool(checked)

        self.filepathLabel.setVisible(self.boxChecked)
        self.filepathLineedit.setVisible(self.boxChecked)
        self.browseButton.setVisible(self.boxChecked)
        self.prefixNameLabel.setVisible(self.boxChecked)
        self.prefixNameLineedit.setVisible(self.boxChecked)
        # self.horizontalspacer
        self.pageLabel.setVisible(self.boxChecked)
        self.pageCombobox.setVisible(self.boxChecked)
        self.formatLabel.setVisible(self.boxChecked)
        self.formatCombobox.setVisible(self.boxChecked)
        self.renderButton.setVisible(self.boxChecked)
        self.normalProgressBar.setVisible(self.boxChecked)

    def setDefaultValues(self):
        self.filepathLineedit.setValue(
            utils.pathResolver(
                self.__parent__.outlineTreewidget.projectPath, folders=[constants.RENDER_FOLDER]
            )
        )

        self.prefixNameLineedit.setCompleters(self.__parent__.outlineTreewidget.headerList)
        self.prefixNameLineedit.setValue(self.__parent__.outlineTreewidget.headerList[0]),

    def getValues(self):
        context = {
            "directory": self.filepathLineedit.value(),
            "prefix": self.prefixNameLineedit.value(),
            "page": self.pageCombobox.value(),
            "format": self.formatCombobox.value(),
        }
        return context

    def clear(self):
        self.filepathLineedit.clear()
        self.prefixNameLineedit.clear()
        self.pageCombobox.setCurrentIndex(0)
        self.formatCombobox.setCurrentIndex(0)

    def startRender(self):
        backgroundFilepath, contextList = self.__parent__.renderContextList()
        renderContext = self.getValues()

        render = media.Render(
            backgroundFilepath, contextList, **renderContext, progressBar=self.renderProgressBar
        )
        render.execute()


if __name__ == "__main__":
    pass
