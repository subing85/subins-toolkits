# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)  Resolver QGroupBox wrapper source code.
# WARNING! All changes made in this file will be lost when recompiling UI file!

from __future__ import absolute_import

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import media
from kore import logger

from widgets.labels import NormalLabel
from widgets.groups import NormalGroup
from widgets.labels import NormalSlider
from widgets.buttons import DiagramButton
from widgets.labels import NormalLineFrame

LOGGER = logger.getLogger(__name__)


class DiagramGroup(NormalGroup):
    def __init__(self, parent, title=None, **kwargs):
        super(DiagramGroup, self).__init__(parent, title=title)

        self.height = kwargs.get("height") or 6.4
        self.width = kwargs.get("width") or 4.0

        self.__parent__ = parent

        self.defaultLayer = media.Layer()
        self.layer = media.Layer()

        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        self.setSizePolicy(sizepolicy)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

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

        self.heightUpFrame = NormalLineFrame(self, shape=QtWidgets.QFrame.VLine)
        self.verticallayout_side.addWidget(self.heightUpFrame)

        self.heightLabel = NormalLabel(self, label=str(self.height), alignment="center")
        self.verticallayout_side.addWidget(self.heightLabel)

        self.heightDownFrame = NormalLineFrame(self, shape=QtWidgets.QFrame.VLine)
        self.verticallayout_side.addWidget(self.heightDownFrame)

        # Width
        self.horizontallayout_down = QtWidgets.QHBoxLayout()
        self.horizontallayout_down.setSpacing(10)
        self.horizontallayout_down.setContentsMargins(10, 10, 10, 10)
        self.gridlayout.addLayout(self.horizontallayout_down, 1, 1, 1, 1)

        self.widthLeftFrame = NormalLineFrame(self, shape=QtWidgets.QFrame.HLine)
        self.horizontallayout_down.addWidget(self.widthLeftFrame)

        self.widthLabel = NormalLabel(self, label=str(self.width), alignment="center")
        self.horizontallayout_down.addWidget(self.widthLabel)

        self.widthRightFrame = NormalLineFrame(self, shape=QtWidgets.QFrame.HLine)
        self.horizontallayout_down.addWidget(self.widthRightFrame)

        # thumbnailButton
        self.diagramButton = DiagramButton(self)

        self.defaultPixmap = self.defaultLayer.setDefault(self.diagramButton.iconpath)
        self.diagramButton.setDiagram(self.defaultPixmap, locked=True)

        self.gridlayout.addWidget(self.diagramButton, 0, 1, 1, 1)

        # Global Scale
        self.horizontallayout_scale = QtWidgets.QHBoxLayout()
        self.verticallayout.addLayout(self.horizontallayout_scale)

        self.scaleLabel = NormalLabel(self, label="Scale", alignment="left")
        self.horizontallayout_scale.addWidget(self.scaleLabel)

        self.scaleSlider = NormalSlider(
            self, "scale", defaultValue=100, minimum=0, maximum=200, pageStep=1
        )

        self.horizontallayout_scale.addWidget(self.scaleSlider)

        # self.verticalspacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.gridlayout.addItem(self.verticalspacer, 3, 1, 1, 1)

    def setLabelSize(self, width, height):
        self.widthLabel.setText(str(round(width, 3)))
        self.heightLabel.setText(str(round(height, 3)))


if __name__ == "__main__":
    pass
