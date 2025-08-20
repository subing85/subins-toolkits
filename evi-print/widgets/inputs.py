# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)  Resolver QWidgets collections source code.
# WARNING! All changes made in this file will be lost when recompiling UI file!

from __future__ import absolute_import

from functools import partial

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import layers
from kore import logger
from kore import stacks

from widgets.labels import NormalVLine
from widgets.labels import NormalHLine
from widgets.labels import NormalLabel
from widgets.labels import NormalSlider
from widgets.buttons import ColorButton
from widgets.buttons import ResetButton
from widgets.buttons import DeleteButton
from widgets.labels import NormalLineEdit
from widgets.spinboxs import NormalSpinBox
from widgets.comboboxs import FontComboBox
from widgets.comboboxs import NormalComboBox
from widgets.spinboxs import NormalDoubleSpinBox


from widgets.buttons import ShapeButton
from widgets.buttons import CenterAlignButtons
from widgets.buttons import MiddleAlignButtons

LOGGER = logger.getLogger(__name__)


class InputSizeWidgets(object):
    def __init__(self, parent, contextList, layout, **kwargs):
        self.__parent__ = parent
        # self.__parent__.diagramGroup = parent.diagramGroup

        self.backgroundImage = None
        self.contextList = contextList

        self.widthDoubleSpinbox = NormalDoubleSpinBox(
            self.__parent__,
            toolTip="Background image X axis",
            minimum=0.0,
            maximum=100,
            step=0.1,
            decimals=3,
            symbols=QtWidgets.QAbstractSpinBox.NoButtons,
            defaultValue=0.0,
        )
        self.widthDoubleSpinbox.setEnabled(False)
        layout.addWidget(self.widthDoubleSpinbox)

        self.heightDoubleSpinbox = NormalDoubleSpinBox(
            self.__parent__,
            toolTip="Background image Y axis",
            minimum=0.0,
            maximum=100,
            step=0.1,
            decimals=3,
            symbols=QtWidgets.QAbstractSpinBox.NoButtons,
            defaultValue=0.0,
        )
        self.heightDoubleSpinbox.setEnabled(False)
        layout.addWidget(self.heightDoubleSpinbox)

        self.sizeCombobox = NormalComboBox(
            self.__parent__, toolTip="Paper sizes", minimumSize=350, maximumSize=350
        )
        self.sizeCombobox.setEnabled(False)
        layout.addWidget(self.sizeCombobox)

        # Resolution columns
        self.resolutionLabel = NormalLabel(
            self.__parent__,
            label="Resolution",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
            minimumSize=100,
        )
        self.resolutionLabel.setEnabled(False)
        layout.addWidget(self.resolutionLabel)

        self.resolutionSpinbox = NormalSpinBox(
            self.__parent__,
            # defaultValue=self.context.get("resolution"),
            toolTip="Backgroud image resolution",
            minimum=75,
            maximum=999999999,
            step=1,
            symbols=QtWidgets.QAbstractSpinBox.NoButtons,
        )
        self.resolutionSpinbox.setEnabled(False)
        layout.addWidget(self.resolutionSpinbox)

    def setBackgroundLayer(self, layer):
        self.backgroundLayer = layer

    def setValue(self, backgroundLayer=None):
        self.setBackgroundLayer(backgroundLayer or self.backgroundLayer)

        width = self.backgroundLayer.widthInInches
        height = self.backgroundLayer.heightInInches

        self.widthDoubleSpinbox.setValue(width)
        self.heightDoubleSpinbox.setValue(height)

        context_list = list(
            filter(lambda x: x["width"] == width and x["height"] == height, self.contextList)
        )

        if context_list:
            currentContext = context_list[0]
        else:
            nullContextList = list(filter(lambda x: x["name"] == "Unknown", self.contextList))
            nullContextList[0]["width"] = width
            nullContextList[0]["height"] = height
            currentContext = nullContextList[0]

        self.sizeCombobox.clear()
        for context in self.contextList:
            self.sizeCombobox.addItem(context["name"])

        self.sizeCombobox.setValue(currentContext["name"])

        self.resolutionSpinbox.setValue(self.backgroundLayer.resolution)

    def value(self):
        inputValues = {
            "width": {"default": self.widthDoubleSpinbox.value()},
            "height": {"default": self.heightDoubleSpinbox.value()},
            "name": {"default": self.sizeCombobox.value()},
            "resolution": {"default": self.resolutionSpinbox.value()},
        }
        return inputValues

    def getValue(self):
        context = {
            "width": self.widthDoubleSpinbox.value(),
            "height": self.heightDoubleSpinbox.value(),
            "name": self.sizeCombobox.value(),
            "resolution": self.resolutionSpinbox.value(),
        }
        return context


class InputPropertyWidgets(object):
    def __init__(self, parent, gridlayout):
        self.__parent__ = parent
        # self.__parent__.diagramGroup = parent.diagramGroup

        self.pause = False

        self.test = False

        self.scaleDefaultValue = 100
        self.maskDefaultValue = 0
        self.strokeDefaultValue = 0
        self.colorDefaultValue = "#000000"

        # Position X columns
        self.positionXLabel = NormalLabel(
            self.__parent__,
            label="Position: X",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
            minimumSize=100,
            maximumSize=100,
        )
        gridlayout.addWidget(self.positionXLabel, 0, 0, 1, 1)

        self.positionXSpinbox = NormalSpinBox(
            self.__parent__,
            toolTip="Foreground image position X parameter",
            step=1,
            symbols=QtWidgets.QAbstractSpinBox.PlusMinus,
            defaultValue=0,
            minimum=-999999999,
            maximum=999999999,
            minimumSize=100,
            maximumSize=100,
        )

        gridlayout.addWidget(self.positionXSpinbox, 0, 1, 1, 1)

        self.positionXSlider = NormalSlider(
            self.__parent__,
            "x",
            defaultValue=0.0,
            minimum=-999999999,
            maximum=999999999,
            spinebox=self.positionXSpinbox,
        )

        # Signal connections
        self.positionXSlider.valueChanged.connect(
            partial(self.setValueChange, self.positionXSpinbox)
        )
        self.positionXSpinbox.valueChanged.connect(
            partial(self.setIndexChange, self.positionXSlider)
        )
        gridlayout.addWidget(self.positionXSlider, 0, 2, 1, 2)

        self.positionXResetButton = ResetButton(self.__parent__)
        # Signal connections
        self.positionXResetButton.clicked.connect(
            partial(self.resetWidegtValue, self.positionXSlider)
        )
        gridlayout.addWidget(self.positionXResetButton, 0, 4, 1, 1)

        # Position Y columns
        self.positionYLabel = NormalLabel(
            self.__parent__,
            label="Y",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        gridlayout.addWidget(self.positionYLabel, 1, 0, 1, 1)

        self.positionYSpinbox = NormalSpinBox(
            self.__parent__,
            toolTip="Foreground image position Y parameter",
            step=1,
            symbols=QtWidgets.QAbstractSpinBox.PlusMinus,
            defaultValue=0,
            minimum=-999999999,
            maximum=999999999,
            minimumSize=100,
            maximumSize=100,
        )
        gridlayout.addWidget(self.positionYSpinbox, 1, 1, 1, 1)

        self.positionYSlider = NormalSlider(
            self.__parent__,
            "y",
            defaultValue=0.0,
            minimum=-999999999,
            maximum=999999999,
            spinebox=self.positionYSpinbox,
        )

        # Signal connections
        self.positionYSlider.valueChanged.connect(
            partial(self.setValueChange, self.positionYSpinbox)
        )
        self.positionYSpinbox.valueChanged.connect(
            partial(self.setIndexChange, self.positionYSlider)
        )
        gridlayout.addWidget(self.positionYSlider, 1, 2, 1, 2)

        self.positionYResetButton = ResetButton(self.__parent__)
        # Signal connections
        self.positionYResetButton.clicked.connect(
            partial(self.resetWidegtValue, self.positionYSlider)
        )
        gridlayout.addWidget(self.positionYResetButton, 1, 4, 1, 1)

        # Position Y align
        self.alignLabel = NormalLabel(
            self.__parent__,
            label="Align",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        gridlayout.addWidget(self.alignLabel, 2, 0, 1, 1)

        self.horizontallayout_align = QtWidgets.QHBoxLayout()
        self.horizontallayout_align.setSpacing(10)
        self.horizontallayout_align.setContentsMargins(10, 10, 10, 10)
        gridlayout.addLayout(self.horizontallayout_align, 2, 2, 1, 2)

        self.centerAlignButtons = CenterAlignButtons(
            self.__parent__, self.horizontallayout_align, align="center"
        )

        self.centerAlignButtons.leftButton.clicked.connect(
            partial(self.setAlignment, self.positionXSlider, "left")
        )
        self.centerAlignButtons.centerButton.clicked.connect(
            partial(self.setAlignment, self.positionXSlider, "center")
        )
        self.centerAlignButtons.rightButton.clicked.connect(
            partial(self.setAlignment, self.positionXSlider, "right")
        )

        self.horizontalSpacer_center = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontallayout_align.addItem(self.horizontalSpacer_center)

        self.middleAlignButtons = MiddleAlignButtons(
            self.__parent__, self.horizontallayout_align, align="middle"
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

        self.horizontalSpacer_middle = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontallayout_align.addItem(self.horizontalSpacer_middle)

        # Scale
        self.scaleLabel = NormalLabel(
            self.__parent__,
            label="Scale",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        gridlayout.addWidget(self.scaleLabel, 3, 0, 1, 1)

        self.scaleSpinbox = NormalSpinBox(
            self.__parent__,
            toolTip="Foreground image scale parameter",
            minimum=0,
            maximum=200,
            step=1,
            symbols=QtWidgets.QAbstractSpinBox.PlusMinus,
            defaultValue=self.scaleDefaultValue,
            minimumSize=100,
            maximumSize=100,
        )
        gridlayout.addWidget(self.scaleSpinbox, 3, 1, 1, 1)

        self.scaleSlider = NormalSlider(
            self.__parent__,
            "scale",
            defaultValue=100,
            minimum=0,
            maximum=200,
            spinebox=self.scaleSpinbox,
        )
        self.scaleSlider.valueChanged.connect(partial(self.setValueChange, self.scaleSpinbox))
        self.scaleSpinbox.valueChanged.connect(partial(self.setIndexChange, self.scaleSlider))
        gridlayout.addWidget(self.scaleSlider, 3, 2, 1, 2)

        self.scaleResetButton = ResetButton(self.__parent__)
        # Signal connections
        self.scaleResetButton.clicked.connect(partial(self.resetWidegtValue, self.scaleSlider))
        gridlayout.addWidget(self.scaleResetButton, 3, 4, 1, 1)

        # Mask
        self.maskLabel = NormalLabel(
            self.__parent__,
            label="Mask",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        gridlayout.addWidget(self.maskLabel, 4, 0, 1, 1)

        self.maskSpinbox = NormalSpinBox(
            self.__parent__,
            toolTip="Foreground image circle mask parameter",
            minimum=0,
            maximum=360,
            step=1,
            symbols=QtWidgets.QAbstractSpinBox.PlusMinus,
            defaultValue=0,
            minimumSize=100,
            maximumSize=100,
        )
        gridlayout.addWidget(self.maskSpinbox, 4, 1, 1, 1)

        self.maskSlider = NormalSlider(
            self.__parent__,
            "mask",
            defaultValue=0,
            minimum=0,
            maximum=360,
            spinebox=self.scaleSpinbox,
        )
        self.maskSlider.valueChanged.connect(partial(self.setValueChange, self.maskSpinbox))
        self.maskSpinbox.valueChanged.connect(partial(self.setIndexChange, self.maskSlider))
        gridlayout.addWidget(self.maskSlider, 4, 2, 1, 1)

        self.shapeButton = ShapeButton(self.__parent__)
        self.shapeButton.clicked.connect(self.setMaskShape)
        gridlayout.addWidget(self.shapeButton, 4, 3, 1, 1)

        self.maskResetButton = ResetButton(self.__parent__)
        # Signal connections
        self.maskResetButton.clicked.connect(partial(self.resetWidegtValue, self.maskSlider))
        gridlayout.addWidget(self.maskResetButton, 4, 4, 1, 1)

        # Stroke
        self.strokeLabel = NormalLabel(
            self.__parent__,
            label="Stroke",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        gridlayout.addWidget(self.strokeLabel, 5, 0, 1, 1)

        self.strokeSpinbox = NormalSpinBox(
            self.__parent__,
            toolTip="Foreground image circle mask parameter",
            minimum=0,
            maximum=100,
            step=1,
            symbols=QtWidgets.QAbstractSpinBox.PlusMinus,
            defaultValue=0,
            minimumSize=100,
            maximumSize=100,
        )
        gridlayout.addWidget(self.strokeSpinbox, 5, 1, 1, 1)

        self.strokeSlider = NormalSlider(self.__parent__, "stroke")
        self.strokeSlider.valueChanged.connect(partial(self.setValueChange, self.strokeSpinbox))
        self.strokeSpinbox.valueChanged.connect(partial(self.setIndexChange, self.strokeSlider))
        gridlayout.addWidget(self.strokeSlider, 5, 2, 1, 1)

        self.strokeColorButton = ColorButton(self.__parent__)
        # Signal connections
        self.strokeColorButton.clicked.connect(self.setStrokeColor)

        gridlayout.addWidget(self.strokeColorButton, 5, 3, 1, 1)

        self.strokeResetButton = ResetButton(self.__parent__)
        # Signal connections
        self.strokeResetButton.clicked.connect(partial(self.resetWidegtValue, self.strokeSlider))
        gridlayout.addWidget(self.strokeResetButton, 5, 4, 1, 1)

    def getValue(self):
        context = {
            "x": self.positionXSpinbox.value(),
            "y": self.positionYSpinbox.value(),
            "scale": self.scaleSpinbox.value(),
            "mask": self.maskSpinbox.value(),
            "shape": self.shapeButton.value(),
            "stroke": self.strokeSpinbox.value(),
            "color": self.strokeColorButton.value(),
        }
        return context

    def setValueChange(self, widget, value):
        if self.pause:
            return

        widget.setValue(value)

    def setIndexChange(self, widget, index):
        # with stacks.Pause(self):
        #     widget.setValue(index)
        #     self.setDiagram()

        if self.pause:
            return

        widget.setValue(index)
        self.setDiagram()

    def setStrokeColor(self):
        if self.pause:
            return

        self.setDiagram()

    def setMaskShape(self):
        if self.pause:
            return

        self.setDiagram()

    def setDiagram(self):
        imageContext = self.getValue()
        self.__parent__.__parent__.foregroundLayer.setContext(**imageContext)
        self.__parent__.__parent__.foregroundLayer.setActive(True)
        pixmap = self.__parent__.composite.setParameters()
        self.__parent__.__parent__.diagramGroup.diagramButton.setDiagram(pixmap, locked=True)

        if self.__parent__.__parent__.currentOutlineItem:
            self.__parent__.__parent__.currentOutlineItem.setOverrideInputContext(imageContext)

    def setAlignment(self, widget, direction):
        foregroundLayer = self.__parent__.__parent__.foregroundLayer

        if not foregroundLayer or not foregroundLayer.isActive:
            LOGGER.warning("Foreground Layer does not active, load foreground image and try")
            return

        alignments = foregroundLayer.getAlignments()
        positionRange = foregroundLayer.getPositionRange()

        widget.setLimits(positionRange[widget.axis][0], positionRange[widget.axis][1])
        widget.spinebox.setLimits(positionRange[widget.axis][0], positionRange[widget.axis][1])

        widget.setValue(alignments[direction][widget.axis])

    def setDefaultValues(self):
        foregroundLayer = self.__parent__.__parent__.foregroundLayer

        if not foregroundLayer or not foregroundLayer.isActive:
            LOGGER.warning("Foreground Layer does not active, load foreground image and try")
            return

        alignments = foregroundLayer.getAlignments()
        positionRange = foregroundLayer.getPositionRange()
        maskValue, maskRange = foregroundLayer.getMaskMaxRange()

        with stacks.Pause(self):
            self.positionXSpinbox.setLimits(positionRange["x"][0], positionRange["x"][1])
            self.positionXSlider.setLimits(positionRange["x"][0], positionRange["x"][1])

            self.positionYSpinbox.setLimits(positionRange["y"][0], positionRange["y"][1])
            self.positionYSlider.setLimits(positionRange["y"][0], positionRange["y"][1])

            self.maskSpinbox.setLimits(maskRange[0], maskRange[1])
            self.maskSlider.setLimits(maskRange[0], maskRange[1])

            self.positionXSpinbox.setDefaultValue(alignments["center"]["x"])
            self.positionYSpinbox.setDefaultValue(alignments["middle"]["y"])

            self.positionXSlider.setDefaultValue(alignments["center"]["x"])
            self.positionYSlider.setDefaultValue(alignments["middle"]["y"])

            self.maskSpinbox.setDefaultValue(maskValue)
            self.maskSlider.setDefaultValue(maskValue)
            # self.positionXSpinbox.setValue(alignments["center"]["x"])
            # self.positionYSpinbox.setValue(alignments["middle"]["y"])

    def resetWidegtValue(self, widget):
        widget.setValues()

    def setValue(self, x, y, scale, mask, shape, stroke, color):
        with stacks.Pause(self):
            self.strokeColorButton.setValue(color)

            self.positionXSpinbox.setValue(x)
            self.positionXSlider.setValue(x)

            self.positionYSpinbox.setValue(y)
            self.positionYSlider.setValue(y)

            self.scaleSpinbox.setValue(scale)
            self.scaleSlider.setValue(scale)

            self.maskSpinbox.setValue(mask)
            self.maskSlider.setValue(mask)

            self.shapeButton.setValue(shape)

            self.strokeSpinbox.setValue(stroke)
            self.strokeSlider.setValue(stroke)

    def _setValueChange(self, widget, value):
        if self.pause:
            return

        # self.pause = True
        widget.setValue(value)
        # self.pause = False

    def _setIndexChange(self, widget, index):
        if self.pause:
            return

        # self.pause = True
        widget.setValue(index)
        # self.pause = False

        self.setDiagram()

    def _setDiagram(self):
        context = self.getValue()

        layer = self.__parent__.__parent__.diagramGroup.layer

        pixmap = layer.setParameters(**context)

        self.__parent__.__parent__.diagramGroup.diagramButton.setDiagram(pixmap, locked=True)

        if self.__parent__.__parent__.currentOutlineItem:
            self.__parent__.__parent__.currentOutlineItem.setOverrideInputContext(context)

    def value(self):
        context = {
            "x": {"default": self.positionXSpinbox.value()},
            "y": {"default": self.positionYSpinbox.value()},
            # "centerAlign": {"value": self.centerAlignButtons.value()},
            # "middleAlign": {"value": self.middleAlignButtons.value()},
            "scale": {"default": self.scaleSpinbox.value()},
            "mask": {"default": self.maskSpinbox.value()},
            "shape": {"default": self.shapeButton.value()},
            "stroke": {"default": self.strokeSpinbox.value()},
            "color": {"default": self.strokeColorButton.value()},
        }
        return context

    def clear(self):
        with stacks.Pause(self):
            self.positionXSpinbox.setDefault()
            self.positionXSlider.setDefault()
            self.positionYSpinbox.setDefault()
            self.positionYSlider.setDefault()
            self.centerAlignButtons.setDefault()
            self.middleAlignButtons.setDefault()
            self.scaleSpinbox.setDefault()
            self.scaleSlider.setDefault()
            self.maskSpinbox.setDefault()
            self.maskSlider.setDefault()
            self.shapeButton.setDefault()
            self.strokeSpinbox.setDefault()
            self.strokeSlider.setDefault()


class InputField(object):
    def __init__(self, parent, index, layout, context, **kwargs):
        self.__parent__ = parent
        self.index = index
        self.layout = layout
        self.context = context

        self.pause = False

        self.isDefault = False

        self.fontFieldDefaultValue = self.context["name"]["value"]
        self.fontValueDefaultValue = self.context["value"]["value"]
        self.fontSizeDefaultValue = self.context["size"]["value"]
        self.fontFamilyDefaultValue = self.context["family"]["value"]
        self.fontTypeDefaultValue = self.context["typed"]["values"]
        self.fontColorDefaultValue = self.context["color"]["value"]
        self.fontXDefaultValue = self.context["x"]["value"]
        self.fontYDefaultValue = self.context["y"]["value"]
        self.fontStrokeDefaultValue = self.context["stroke"]["value"]
        self.fontStrokeColorDefaultValue = self.context["strokeColor"]["value"]
        self.fontSpaceDefaultValue = self.context["space"]["value"]

        # self.textLayer = layers.TextLayer(self.__parent__.__parent__.diagramGroup.layer.backgroundLayer, self.index)
        self.textLayer = layers.TextLayer(self.index)
        self.__parent__.composite.addTextLayer(self.index, self.textLayer)

        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout.setVerticalSpacing(20)
        self.gridlayout.setHorizontalSpacing(10)
        self.gridlayout.setContentsMargins(10, 10, 10, 10)

        self.layout.addLayout(self.gridlayout)

        # Field Name

        self.fieldLabel = NormalLabel(
            self.__parent__,
            label="Field",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Fixed,
            veritcalPolicy=QtWidgets.QSizePolicy.Preferred,
        )
        self.gridlayout.addWidget(self.fieldLabel, 0, 0, 1, 1)

        self.fieldLineEdit = NormalLineEdit(
            self.__parent__,
            label=self.fontFieldDefaultValue,
            minimumSize=100,
            horizontalPolicy=QtWidgets.QSizePolicy.Fixed,
            veritcalPolicy=QtWidgets.QSizePolicy.Preferred,
        )
        self.gridlayout.addWidget(self.fieldLineEdit, 0, 1, 1, 1)

        # Field Value
        self.valueLabel = NormalLabel(
            self.__parent__,
            label="Value",
            alignment="right",
            minimumSize=70,
            horizontalPolicy=QtWidgets.QSizePolicy.Fixed,
            veritcalPolicy=QtWidgets.QSizePolicy.Preferred,
        )
        self.gridlayout.addWidget(self.valueLabel, 0, 2, 1, 1)

        self.valueLineEdit = NormalLineEdit(
            self.__parent__,
            label=self.fontValueDefaultValue,
            minimumSize=100,
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Fixed,
        )
        # self.valueLineEdit.editingFinished.connect(partial(self.setText, None))
        self.valueLineEdit.textChanged.connect(partial(self.setText, None))

        self.gridlayout.addWidget(self.valueLineEdit, 0, 3, 1, 2)

        self.line_value = NormalVLine(self.__parent__)
        self.gridlayout.addWidget(self.line_value, 0, 5, 1, 1)

        # Font
        self.fontLabel = NormalLabel(
            self.__parent__,
            label="Font",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Fixed,
            veritcalPolicy=QtWidgets.QSizePolicy.Preferred,
            minimumSize=70,
        )
        self.gridlayout.addWidget(self.fontLabel, 0, 6, 1, 1)

        self.sizeSpinbox = NormalSpinBox(
            self.__parent__,
            toolTip="Text font size parameter",
            minimum=0,
            maximum=200,
            step=1,
            # decimals=2,
            symbols=QtWidgets.QAbstractSpinBox.PlusMinus,
            defaultValue=self.fontSizeDefaultValue,
            minimumSize=100,
            maximumSize=150,
        )
        self.sizeSpinbox.valueChanged.connect(partial(self.setText, None))
        self.gridlayout.addWidget(self.sizeSpinbox, 0, 7, 1, 1)

        self.fontFamilyCombobox = FontComboBox(
            self.__parent__,
            currentFonts=self.fontFamilyDefaultValue,
            minimumSize=150,
        )
        self.fontFamilyCombobox.currentFontChanged.connect(self.setText)
        self.gridlayout.addWidget(self.fontFamilyCombobox, 0, 8, 1, 2)

        self.colorButton = ColorButton(self.__parent__, color=self.fontColorDefaultValue)
        self.colorButton.clicked.connect(self.setText)
        self.gridlayout.addWidget(self.colorButton, 0, 10, 1, 1)

        self.line_font = NormalVLine(self.__parent__)
        self.gridlayout.addWidget(self.line_font, 0, 11, 1, 1)

        self.resetButton = ResetButton(self.__parent__)
        self.gridlayout.addWidget(self.resetButton, 0, 12, 1, 1)

        self.deleteButton = DeleteButton(self.__parent__)
        self.gridlayout.addWidget(self.deleteButton, 0, 13, 1, 1)

        # Stroke
        self.strokeLabel = NormalLabel(
            self.__parent__,
            label="Stroke",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Preferred,
        )
        self.gridlayout.addWidget(self.strokeLabel, 1, 1, 1, 1)

        self.strokeSpinBox = NormalSpinBox(
            self.__parent__,
            toolTip="Text stroke width",
            minimum=0,
            maximum=100,
            step=1,
            symbols=QtWidgets.QAbstractSpinBox.PlusMinus,
            defaultValue=self.fontStrokeDefaultValue,
            minimumSize=100,
            maximumSize=150,
        )
        self.strokeSpinBox.valueChanged.connect(partial(self.setText, None))
        self.gridlayout.addWidget(self.strokeSpinBox, 1, 2, 1, 2)

        self.strokeColorButton = ColorButton(
            self.__parent__, color=self.fontStrokeColorDefaultValue
        )
        self.strokeColorButton.clicked.connect(self.setText)
        self.gridlayout.addWidget(self.strokeColorButton, 1, 4, 1, 1)

        self.line_stroke = NormalVLine(self.__parent__)
        self.gridlayout.addWidget(self.line_stroke, 1, 5, 1, 1)

        self.spaceLabel = NormalLabel(
            self.__parent__,
            label="Space",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Fixed,
            veritcalPolicy=QtWidgets.QSizePolicy.Preferred,
            minimumSize=70,
        )
        self.gridlayout.addWidget(self.spaceLabel, 1, 6, 1, 1)

        self.spaceSpinBox = NormalSpinBox(
            self.__parent__,
            toolTip="Text space",
            minimum=0,
            maximum=1000,
            step=1,
            symbols=QtWidgets.QAbstractSpinBox.PlusMinus,
            defaultValue=self.fontSpaceDefaultValue,
            minimumSize=100,
            maximumSize=150,
        )
        self.spaceSpinBox.valueChanged.connect(partial(self.setText, None))
        self.gridlayout.addWidget(self.spaceSpinBox, 1, 7, 1, 1)

        self.horizontallayout_align = QtWidgets.QHBoxLayout()
        self.horizontallayout_align.setSpacing(10)
        self.horizontallayout_align.setContentsMargins(0, 0, 0, 0)
        self.gridlayout.addLayout(self.horizontallayout_align, 1, 8, 1, 1)

        self.centerAlignButtons = CenterAlignButtons(
            self.__parent__, self.horizontallayout_align, align="left"
        )
        self.centerAlignButtons.leftButton.clicked.connect(self.setAlignment)
        self.centerAlignButtons.centerButton.clicked.connect(self.setAlignment)
        self.centerAlignButtons.rightButton.clicked.connect(self.setAlignment)

        self.horizontalspacer_space = QtWidgets.QSpacerItem(
            248, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridlayout.addItem(self.horizontalspacer_space, 1, 9, 1, 5)

        # Position
        self.positionXLabel = NormalLabel(
            self.__parent__,
            label=" Position X",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Preferred,
        )

        self.gridlayout.addWidget(self.positionXLabel, 2, 1, 1, 1)

        self.positionXSpinbox = NormalSpinBox(
            self.__parent__,
            toolTip="Text position X parameter",
            minimum=-999999999,
            maximum=999999999,
            step=1,
            symbols=QtWidgets.QAbstractSpinBox.PlusMinus,
            defaultValue=self.fontXDefaultValue,
            minimumSize=100,
            maximumSize=150,
        )
        self.gridlayout.addWidget(self.positionXSpinbox, 2, 2, 1, 2)

        self.positionXSlider = NormalSlider(
            self.__parent__,
            "x",
            defaultValue=self.context["x"]["value"],
            minimum=-999999999,
            maximum=999999999,
            spinebox=self.positionXSpinbox,
        )
        self.positionXSlider.valueChanged.connect(
            partial(self.setValueChange, self.positionXSpinbox)
        )
        self.positionXSpinbox.valueChanged.connect(
            partial(self.setIndexChange, self.positionXSlider)
        )
        self.gridlayout.addWidget(self.positionXSlider, 2, 4, 1, 7)

        self.positionXResetButton = ResetButton(self.__parent__)
        # Signal connections
        self.positionXResetButton.clicked.connect(
            partial(self.resetWidegtValue, self.positionXSlider)
        )
        self.gridlayout.addWidget(self.positionXResetButton, 2, 11, 1, 3)

        # self.horizontalspacer_x = QtWidgets.QSpacerItem(168, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.gridlayout.addItem(self.horizontalspacer_x, 2, 11, 1, 3)

        self.positionYLabel = NormalLabel(
            self.__parent__,
            label="Y",
            alignment="right",
            horizontalPolicy=QtWidgets.QSizePolicy.Preferred,
            veritcalPolicy=QtWidgets.QSizePolicy.Preferred,
        )

        self.gridlayout.addWidget(self.positionYLabel, 3, 1, 1, 1)

        self.positionYSpinbox = NormalSpinBox(
            self.__parent__,
            toolTip="Text position Y parameter",
            minimum=-999999999,
            maximum=999999999,
            step=1,
            symbols=QtWidgets.QAbstractSpinBox.PlusMinus,
            defaultValue=self.fontYDefaultValue,
            minimumSize=100,
            maximumSize=150,
        )

        self.gridlayout.addWidget(self.positionYSpinbox, 3, 2, 1, 2)

        self.positionYSlider = NormalSlider(
            self.__parent__,
            "y",
            defaultValue=self.context["y"]["value"],
            minimum=-999999999,
            maximum=999999999,
            spinebox=self.positionYSpinbox,
        )
        self.positionYSlider.valueChanged.connect(
            partial(self.setValueChange, self.positionYSpinbox)
        )
        self.positionYSpinbox.valueChanged.connect(
            partial(self.setIndexChange, self.positionYSlider)
        )
        self.gridlayout.addWidget(self.positionYSlider, 3, 4, 1, 7)

        self.positionYResetButton = ResetButton(self.__parent__)
        # Signal connections
        self.positionYResetButton.clicked.connect(
            partial(self.resetWidegtValue, self.positionYSlider)
        )
        self.gridlayout.addWidget(self.positionYResetButton, 3, 11, 1, 3)

        # self.horizontalspacer_y = QtWidgets.QSpacerItem(168, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.gridlayout.addItem(self.horizontalspacer_y, 3, 11, 1, 3)

        self.spearateLine = NormalHLine(self.__parent__)
        self.layout.addWidget(self.spearateLine)

    def deleteLater(self):
        self.fieldLabel.deleteLater()
        self.fieldLineEdit.deleteLater()
        self.valueLabel.deleteLater()
        self.valueLineEdit.deleteLater()
        self.line_value.deleteLater()

        # Font
        self.fontLabel.deleteLater()
        self.sizeSpinbox.deleteLater()
        self.fontFamilyCombobox.deleteLater()
        self.colorButton.deleteLater()
        self.line_font.deleteLater()
        self.resetButton.deleteLater()
        self.deleteButton.deleteLater()

        self.strokeLabel.deleteLater()
        self.strokeSpinBox.deleteLater()
        self.strokeColorButton.deleteLater()
        self.line_stroke.deleteLater()
        self.spaceLabel.deleteLater()
        self.spaceSpinBox.deleteLater()

        self.centerAlignButtons.deleteLater()
        self.horizontallayout_align.deleteLater()

        # self.horizontalspacer_space.deleteLater()

        del self.horizontalspacer_space

        self.positionXLabel.deleteLater()
        self.positionXSpinbox.deleteLater()
        self.positionXSlider.deleteLater()

        # self.horizontalspacer_x.deleteLater()
        # del self.horizontalspacer_x

        self.positionYLabel.deleteLater()
        self.positionYSpinbox.deleteLater()
        self.positionYSlider.deleteLater()

        # self.horizontalspacer_y.deleteLater()
        # del self.horizontalspacer_y

        self.spearateLine.deleteLater()

        self.gridlayout.deleteLater()

    def setDefaultValues(self):  # new Final #######################
        alignments = self.textLayer.getAlignments()
        positionRange = self.textLayer.getPositionRange()

        with stacks.Pause(self):
            self.positionXSpinbox.setLimits(positionRange["x"][0], positionRange["x"][1])
            self.positionXSlider.setLimits(positionRange["x"][0], positionRange["x"][1])

            self.positionYSpinbox.setLimits(positionRange["y"][0], positionRange["y"][1])
            self.positionYSlider.setLimits(positionRange["y"][0], positionRange["y"][1])

            self.positionXSpinbox.setDefaultValue(alignments["center"]["x"])
            self.positionYSpinbox.setDefaultValue(alignments["middle"]["y"])

            self.positionXSlider.setDefaultValue(alignments["center"]["x"])
            self.positionYSlider.setDefaultValue(alignments["middle"]["y"])

            # self.positionXSpinbox.setValue(alignments["center"]["x"])
            # self.positionYSpinbox.setValue(alignments["middle"]["y"])

            self.isDefault = True

    def setValueChange(self, widget, value):
        if self.pause:
            return
        widget.setValue(value)

    def setIndexChange(self, widget, index):
        # with stacks.Pause(self):
        #     widget.setValue(index)
        #     self.setDiagram()

        if self.pause:
            return

        widget.setValue(index)
        self.setDiagram()

    def setText(self, *args):
        if self.pause:
            return

        self.setDiagram()
        self.setDefaultValues()

    def setAlignment(self):  # old Final #######################
        direction = self.centerAlignButtons.value()

        if self.index > 0:
            previousInputField = self.__parent__.children[self.index - 1]
            previousBoundingBox = previousInputField.textLayer.boundingBox
            x = previousBoundingBox.x()
            width = previousBoundingBox.width()
        else:
            # previousBoundingBox = self.__parent__.__parent__.diagramGroup.layer.backgroundLayer
            previousBoundingBox = self.textLayer.backgroundImage

            x = 0
            width = previousBoundingBox.width()

        currentBoundingBox = self.textLayer.boundingBox

        if direction == "left":
            value = x

        if direction == "center":
            value = (x + (width / 2)) - (currentBoundingBox.width() / 2)

        if direction == "right":
            value = (x + width) - currentBoundingBox.width()

        self.positionXSlider.setValue(value)

    def resetWidegtValue(self, widget):
        widget.setValues()

    def getValue(self):
        textLayerContext = {
            "text": self.valueLineEdit.value(),
            "size": self.sizeSpinbox.value(),
            "family": self.fontFamilyCombobox.value(),
            "type": None,
            "fillColor": self.colorButton.value(),
            "x": self.positionXSpinbox.value(),
            "y": self.positionYSpinbox.value(),
            "stroke": self.strokeSpinBox.value(),
            "strokeColor": self.strokeColorButton.value(),
            "spacing": self.spaceSpinBox.value(),
        }
        return textLayerContext

    def setDiagram(self):  # old Final #######################
        # self.setTextLayerContext()

        textLayerContext = self.getValue()
        self.textLayer.setContext(**textLayerContext)
        self.textLayer.setActive(True)
        pixmap = self.__parent__.composite.setParameters()
        self.__parent__.__parent__.diagramGroup.diagramButton.setDiagram(pixmap, locked=True)

        if self.__parent__.__parent__.currentOutlineItem:
            self.__parent__.__parent__.currentOutlineItem.setOverrideFieldContext(
                self.index, textLayerContext
            )

    def setContext(self):  # New Final #######################
        textLayerContext = self.getValue()
        self.textLayer.setContext(**textLayerContext)
        return textLayerContext

    def _setValueChange(self, widget, value):
        if self.pause:
            return

        # self.pause = True
        widget.setValue(value)
        # self.pause = False

    def _setIndexChange(self, widget, index):
        if self.pause:
            return

        # self.pause = True
        widget.setValue(index)
        # self.pause = False

        self.setDiagram()

    def setValue(self, *args):
        field = args[0]
        text = args[1]
        size = args[2]
        family = args[3]
        color = args[4]
        stroke = args[5]
        strokeColor = args[6]
        spacing = args[7]
        x = args[8]
        y = args[9]

        bold = args[10]
        italic = args[11]
        underline = args[12]
        overline = args[13]
        strikeOut = args[14]

        wordSpacing = args[15]
        stretch = args[16]
        capitalization = args[17]

        with stacks.Pause(self):
            self.fieldLineEdit.setValue(field)
            self.valueLineEdit.setValue(text)

            self.sizeSpinbox.setValue(size)
            self.fontFamilyCombobox.setValue(family)

            self.colorButton.setValue(color)
            self.strokeSpinBox.setValue(stroke)
            self.strokeColorButton.setValue(strokeColor)

            self.spaceSpinBox.setValue(spacing)

            self.positionXSlider.setValue(x)
            self.positionXSpinbox.setValue(x)

            self.positionYSlider.setValue(y)
            self.positionYSpinbox.setValue(y)


if __name__ == "__main__":
    pass
