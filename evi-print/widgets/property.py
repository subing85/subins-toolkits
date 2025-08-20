# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)  Resolver QGroupBox wrapper source code.
# WARNING! All changes made in this file will be lost when recompiling UI file!

from __future__ import absolute_import

from functools import partial

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import utils
from kore import logger

from widgets.groups import NormalGroup
from widgets.labels import NormalLabel
from widgets.buttons import ResetButton
from widgets.labels import NormalLineEdit
from widgets.spinboxs import NormalSpinBox
from widgets.buttons import BrowseFileButton


LOGGER = logger.getLogger(__name__)


class PropertyGroup(NormalGroup):
    def __init__(self, parent, title=None, **kwargs):
        super(PropertyGroup, self).__init__(parent, title=title)

        self.height = kwargs.get("height") or "6.4"
        self.width = kwargs.get("width") or "4.0"
        self.context = kwargs.get("context")

        self.__parent__ = parent

        # self.diagramLayer = media.Layer()

        self.setMinimumSize(QtCore.QSize(400, 0))
        # self.setMaximumSize(QtCore.QSize(400, 16777215))

        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.setSizePolicy(sizepolicy)

        self.gridlayout = QtWidgets.QGridLayout(self)
        self.gridlayout.setVerticalSpacing(10)
        self.gridlayout.setHorizontalSpacing(10)
        self.gridlayout.setContentsMargins(10, 10, 10, 10)

        # Resolution columns
        self.resolutionLabel = NormalLabel(self, label="Resolution", alignment="right")
        self.gridlayout.addWidget(self.resolutionLabel, 0, 0, 1, 1)

        self.resolutionSpinbox = NormalSpinBox(
            self,
            defaultValue=self.context.get("resolution"),
            toolTip="Backgroud image resolution",
            minimum=75,
            maximum=999999999,
            step=1,
            symbols=QtWidgets.QAbstractSpinBox.PlusMinus,
        )
        self.gridlayout.addWidget(self.resolutionSpinbox, 0, 1, 1, 2)

        self.spacer_resolution_1 = QtWidgets.QSpacerItem(
            295, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridlayout.addItem(self.spacer_resolution_1, 0, 3, 1, 3)

        self.resolutionResetButton = ResetButton(self)
        self.resolutionResetButton.clicked.connect(
            partial(self.resetWidegtValue, self.resolutionSpinbox)
        )
        self.gridlayout.addWidget(self.resolutionResetButton, 0, 6, 1, 1)

        # Size columns
        self.sizeGroup = SizeGroup(self, self.context["size"], self.gridlayout, 1)

        self.sizeResetButton = ResetButton(self)
        self.sizeResetButton.clicked.connect(partial(self.resetWidegtValue, self.sizeGroup))
        self.gridlayout.addWidget(self.sizeResetButton, 1, 6, 1, 1)

        # background image columns
        self.backgroundLabel = NormalLabel(self, label="Backgroud", alignment="right")
        self.gridlayout.addWidget(self.backgroundLabel, 2, 0, 1, 1)

        self.backgroundLineedit = NormalLineEdit(self)
        self.gridlayout.addWidget(self.backgroundLineedit, 2, 1, 1, 4)

        self.backgroundBrowseButton = BrowseFileButton(
            self, widget=self.backgroundLineedit, formats=["png", "jpg", "jpeg", "tga"]
        )
        self.gridlayout.addWidget(self.backgroundBrowseButton, 2, 5, 1, 1)

        self.backgroundResetButton = ResetButton(self)
        self.backgroundResetButton.clicked.connect(
            partial(self.resetWidegtValue, self.backgroundLineedit)
        )
        self.gridlayout.addWidget(self.backgroundResetButton, 2, 6, 1, 1)

        # Foreground image columns
        self.foregroundLabel = NormalLabel(self, label="Forground", alignment="right")
        self.gridlayout.addWidget(self.foregroundLabel, 3, 0, 1, 1)

        self.foregroundLineedit = NormalLineEdit(self)
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

        self.foregroundGroup = ForegroundGroup(self, self.gridlayout_foreground)

        # Set default background image
        # self.setBackground()

    def resetWidegtValue(self, widget):
        widget.setDefaultValue()

    def setBackground(self, diagramGroup):
        filepath = self.backgroundLineedit.values()

        filepath = filepath or None

        if filepath is None:
            pixmap = diagramGroup.defaultPixmap
            layer = diagramGroup.defaultLayer

        else:
            if not utils.hasFileExists(filepath):
                QtWidgets.QMessageBox.warning(
                    self, "Warning", "Invalid source background file path", QtGui.QMessageBox.Close
                )
                LOGGER.warning("Invalid source background file path")
                return

            pixmap = diagramGroup.layer.setBackground(filepath)
            layer = diagramGroup.layer

        self.resolutionSpinbox.setDefaultValue(layer.backgroundLayer.dpi[0])

        # print(layer.backgroundLayer.widthInInches, layer.backgroundLayer.heightInInches)

        diagramGroup.diagramButton.setDiagram(pixmap, locked=True)
        diagramGroup.setLabelSize(
            layer.backgroundLayer.widthInInches, layer.backgroundLayer.heightInInches
        )

        # self.sizeGroup.setSize(width=layer.backgroundLayer.widthInInches, height=layer.backgroundLayer.heightInInches)

    def setForeground(self, diagramGroup):
        filepath = self.foregroundLineedit.values()

        if filepath is None:
            layer = diagramGroup.defaultLayer

        else:
            if not utils.hasFileExists(filepath):
                QtWidgets.QMessageBox.warning(
                    self, "Warning", "Invalid source foreground file path", QtGui.QMessageBox.Close
                )
                LOGGER.warning("Invalid source foreground file path")
                return

            layer = diagramGroup.layer

        pixmap = layer.addForeground(filepath)

        centerPosition, centerRange = layer.alignment("center")
        middlePosition, middleRange = layer.alignment("middle")

        self.foregroundGroup.positionWidthSpinbox.setValue(centerPosition["width"])
        self.foregroundGroup.positionHeightSpinbox.setValue(middlePosition["height"])

        self.foregroundGroup.positionWidthSpinbox.setLimits(
            centerRange["width"][0], centerRange["width"][1]
        )
        self.foregroundGroup.positionWidthSlider.setLimits(
            centerRange["width"][0], centerRange["width"][1]
        )

        self.foregroundGroup.positionHeightSpinbox.setLimits(
            middleRange["height"][0], middleRange["height"][1]
        )
        self.foregroundGroup.positionHeightSlider.setLimits(
            middleRange["height"][0], middleRange["height"][1]
        )


if __name__ == "__main__":
    pass
