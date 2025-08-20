# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)  Resolver QSpinbox and QDoubleSpinBox wrapper source code.
# WARNING! All changes made in this file will be lost when recompiling UI file!

from __future__ import absolute_import


from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets


class NormalSpinBox(QtWidgets.QSpinBox):
    def __init__(self, parent, **kwargs):
        super(NormalSpinBox, self).__init__(parent)

        self.defaultValue = kwargs.get("defaultValue") or 0

        self.toolTip = kwargs.get("toolTip")
        self.minimum = kwargs.get("minimum") or 0
        self.maximum = kwargs.get("maximum") or 100
        self.step = kwargs.get("step") or 1
        self.symbols = kwargs.get("symbols") or QtWidgets.QAbstractSpinBox.NoButtons
        # QAbstractSpinBox.UpDownArrows QAbstractSpinBox.PlusMinus
        self.minimumSize = kwargs.get("minimumSize")
        self.maximumSize = kwargs.get("maximumSize")

        self.setToolTip(self.toolTip)
        self.setMinimum(self.minimum)
        self.setMaximum(self.maximum)
        self.setButtonSymbols(self.symbols)
        self.setSingleStep(self.step)
        self.setValue(self.defaultValue)

        if self.minimumSize:
            self.setMinimumSize(QtCore.QSize(self.minimumSize, 0))
        if self.maximumSize:
            self.setMaximumSize(QtCore.QSize(self.maximumSize, 16777215))

        sizepolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(sizepolicy)

    def setDefaultValue(self, value):
        self.defaultValue = value

    def setValues(self, value=None):
        self.setValue(value or self.defaultValue)

    def setLimits(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

        self.setMinimum(self.minimum)
        self.setMaximum(self.maximum)

    def setDefault(self):
        self.setValue(self.defaultValue)


class NormalDoubleSpinBox(QtWidgets.QDoubleSpinBox):
    def __init__(self, parent, **kwargs):
        super(NormalDoubleSpinBox, self).__init__(parent)

        self.defaultValue = kwargs.get("defaultValue") or 0
        self.toolTip = kwargs.get("toolTip")
        self.minimum = kwargs.get("minimum") or 0
        self.maximum = kwargs.get("maximum") or 100
        self.step = kwargs.get("step") or 1
        self.decimals = kwargs.get("decimals") or 2
        self.symbols = kwargs.get("symbols") or QtWidgets.QAbstractSpinBox.NoButtons
        # QAbstractSpinBox.UpDownArrows QAbstractSpinBox.PlusMinus
        self.minimumSize = kwargs.get("minimumSize")
        self.maximumSize = kwargs.get("maximumSize")

        self.setToolTip(self.toolTip)
        self.setMinimum(self.minimum)
        self.setMaximum(self.maximum)
        self.setButtonSymbols(self.symbols)
        self.setSingleStep(self.step)
        self.setDecimals(self.decimals)
        self.setValue(self.defaultValue)

        if self.minimumSize:
            self.setMinimumSize(QtCore.QSize(self.minimumSize, 0))
        if self.maximumSize:
            self.setMaximumSize(QtCore.QSize(self.maximumSize, 16777215))

        sizepolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(sizepolicy)

    def setDefaultValue(self, value):
        self.defaultValue = value

    def setValues(self, value=None):
        self.setValue(value or self.defaultValue)

    def setLimits(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

        self.setMinimum(self.minimum)
        self.setMaximum(self.maximum)

    def setDefault(self):
        self.setValue(self.defaultValue)


class SizeSpinbox(NormalDoubleSpinBox):
    def __init__(self, parent, **kwargs):
        super(SizeSpinbox, self).__init__(parent)


if __name__ == "__main__":
    pass
