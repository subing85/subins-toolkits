# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)  Resolver QLabel and QLineEdit wrapper source code.
# WARNING! All changes made in this file will be lost when recompiling UI file!

from __future__ import absolute_import

import widgets

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import utils


class CopyrightLabel(QtWidgets.QLabel):
    def __init__(self, parent, **kwargs):
        super(CopyrightLabel, self).__init__(parent)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        self.setSizePolicy(sizePolicy)
        widgets.setFontSize(self, 9, family="Arial", bold=False)

        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.setText("Copyright (c) 2023, Jackfruit-Studio Production All rights reserved.")


class NormalLabel(QtWidgets.QLabel):
    def __init__(self, parent, **kwargs):
        super(NormalLabel, self).__init__(parent)

        self.label = kwargs.get("label")

        if kwargs.get("alignment") == "right":
            self.alignment = QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        elif kwargs.get("alignment") == "left":
            self.alignment = QtCore.Qt.AlignLeft | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        else:
            self.alignment = QtCore.Qt.AlignCenter

        self.minimumSize = kwargs.get("minimumSize")
        self.maximumSize = kwargs.get("maximumSize")

        self.horizontalPolicy = (
            QtWidgets.QSizePolicy.Preferred
            if kwargs.get("horizontalPolicy") is None
            else kwargs.get("horizontalPolicy", QtWidgets.QSizePolicy.Preferred)
        )

        self.veritcalPolicy = (
            QtWidgets.QSizePolicy.Preferred
            if kwargs.get("veritcalPolicy") is None
            else kwargs.get("veritcalPolicy", QtWidgets.QSizePolicy.Preferred)
        )

        if self.minimumSize:
            self.setMinimumSize(QtCore.QSize(self.minimumSize, 0))
        if self.maximumSize:
            self.setMaximumSize(QtCore.QSize(self.maximumSize, 16777215))

        sizepolicy = QtWidgets.QSizePolicy(self.horizontalPolicy, self.veritcalPolicy)
        self.setSizePolicy(sizepolicy)

        # widgets.setFontSize(self, 9, family="Arial", bold=False)

        self.setAlignment(self.alignment)
        self.setText(self.label)

    def setValue(self, value):
        self.setText(value)


class ZoomLabel(QtWidgets.QLabel):
    def __init__(self, parent, **kwargs):
        super(ZoomLabel, self).__init__(parent)

        self.value = kwargs.get("value") or 100

        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        self.setSizePolicy(sizepolicy)

        self.setValue(self.value)

    def setValue(self, value):
        self.setText("Zoom ( %s %s)" % (value, "%"))


class NormalLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent, **kwargs):
        super(NormalLineEdit, self).__init__(parent)

        self.label = kwargs.get("label")

        self.defaultValue = kwargs.get("label")

        self.minimumSize = kwargs.get("minimumSize")
        self.maximumSize = kwargs.get("maximumSize")

        self.horizontalPolicy = (
            QtWidgets.QSizePolicy.Preferred
            if kwargs.get("horizontalPolicy") is None
            else kwargs.get("horizontalPolicy", QtWidgets.QSizePolicy.Preferred)
        )

        self.veritcalPolicy = (
            QtWidgets.QSizePolicy.Fixed
            if kwargs.get("veritcalPolicy") is None
            else kwargs.get("veritcalPolicy", QtWidgets.QSizePolicy.Fixed)
        )

        if self.minimumSize:
            self.setMinimumSize(QtCore.QSize(self.minimumSize, 0))
        if self.maximumSize:
            self.setMaximumSize(QtCore.QSize(self.maximumSize, 16777215))

        sizepolicy = QtWidgets.QSizePolicy(self.horizontalPolicy, self.veritcalPolicy)

        self.setSizePolicy(sizepolicy)

        if self.label:
            self.setText(self.label)

    def setDefaultValue(self, value):
        self.defaultValue = value
        # self.setText(self.defaultValue)

    def setValue(self, value=None):
        self.setText(value or self.defaultValue)

    def value(self):
        return self.text()


class PrefixNameLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent, **kwargs):
        super(PrefixNameLineEdit, self).__init__(parent)
        self.minimumSize = kwargs.get("minimumSize")
        self.maximumSize = kwargs.get("maximumSize")

        self.modelList = list()

        if self.minimumSize:
            self.setMinimumSize(QtCore.QSize(self.minimumSize, 0))
        if self.maximumSize:
            self.setMaximumSize(QtCore.QSize(self.maximumSize, 16777215))

    def setCompleters(self, modelList):
        self.modelList = modelList

        self.completerModel = QtCore.QStringListModel(self.modelList)
        self.completer = QtWidgets.QCompleter()
        self.completer.setModel(self.completerModel)
        self.setCompleter(self.completer)

    def setValue(self, value):
        self.setText(value)

    def value(self):
        name = self.text()

        if name not in self.modelList:
            return name or None

        return self.modelList.index(name)


class NormalSlider(QtWidgets.QSlider):
    def __init__(self, parent, axis, **kwargs):
        super(NormalSlider, self).__init__(parent)

        self.axis = axis
        self.toolTip = kwargs.get("toolTip")
        self.minimum = kwargs.get("minimum") or 0
        self.maximum = kwargs.get("maximum") or 100
        self.pageStep = kwargs.get("pageStep") or 1
        self.tickInterval = kwargs.get("tickInterval") or 10

        self.defaultValue = kwargs.get("defaultValue") or 0
        self.spinebox = kwargs.get("spinebox")

        self.horizontalPolicy = (
            QtWidgets.QSizePolicy.Preferred
            if kwargs.get("horizontalPolicy") is None
            else kwargs.get("horizontalPolicy", QtWidgets.QSizePolicy.Preferred)
        )

        self.veritcalPolicy = (
            QtWidgets.QSizePolicy.Fixed
            if kwargs.get("veritcalPolicy") is None
            else kwargs.get("veritcalPolicy", QtWidgets.QSizePolicy.Fixed)
        )

        self.setToolTip(self.toolTip)
        self.setMinimum(self.minimum)
        self.setMaximum(self.maximum)
        self.setPageStep(self.pageStep)
        self.setOrientation(QtCore.Qt.Horizontal)

        self.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.setTickInterval(self.tickInterval)
        self.setValue(self.defaultValue)

        sizepolicy = QtWidgets.QSizePolicy(self.horizontalPolicy, self.veritcalPolicy)
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


class NormalVLine(QtWidgets.QFrame):
    def __init__(self, parent, **kwargs):
        super(NormalVLine, self).__init__(parent)

        self.horizontalPolicy = (
            QtWidgets.QSizePolicy.Fixed
            if kwargs.get("horizontalPolicy") is None
            else kwargs.get("horizontalPolicy", QtWidgets.QSizePolicy.Fixed)
        )

        self.veritcalPolicy = (
            QtWidgets.QSizePolicy.Minimum
            if kwargs.get("veritcalPolicy") is None
            else kwargs.get("veritcalPolicy", QtWidgets.QSizePolicy.Minimum)
        )

        self.setStyleSheet("background-color: rgb(80, 80, 80);")

        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

        sizepolicy = QtWidgets.QSizePolicy(self.horizontalPolicy, self.veritcalPolicy)

        self.setSizePolicy(sizepolicy)


class NormalHLine(QtWidgets.QFrame):
    def __init__(self, parent, **kwargs):
        super(NormalHLine, self).__init__(parent)

        self.horizontalPolicy = (
            QtWidgets.QSizePolicy.Minimum
            if kwargs.get("horizontalPolicy") is None
            else kwargs.get("horizontalPolicy", QtWidgets.QSizePolicy.Minimum)
        )

        self.veritcalPolicy = (
            QtWidgets.QSizePolicy.Fixed
            if kwargs.get("veritcalPolicy") is None
            else kwargs.get("veritcalPolicy", QtWidgets.QSizePolicy.Fixed)
        )

        self.setStyleSheet("background-color: rgb(80, 80, 80);")

        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

        sizepolicy = QtWidgets.QSizePolicy(self.horizontalPolicy, self.veritcalPolicy)

        self.setSizePolicy(sizepolicy)


class NormalProgressBar(QtWidgets.QProgressBar):
    def __init__(self, parent, **kwargs):
        super(NormalProgressBar, self).__init__(parent)

        self.setStyleSheet(
            "QProgressBar::chunk {background-color: rgb(205, 150, 205);width: 2px;margin: 0.5px;}"
        )

        # self.setMinimumSize(QtCore.QSize(0, 20))
        # self.setMaximumSize(QtCore.QSize(16777215, 20))

        self.setFormat("%p%")

        self.setValue(0)

    def reset(self):
        self.setFormat("%p%")

    def setValues(self, index, value):
        self.setValue(index)
        self.setFormat("{} %p%".format(value))


class NormalCheckbox(QtWidgets.QCheckBox):
    def __init__(self, parent, **kwargs):
        super(NormalCheckbox, self).__init__(parent)

        self.label = kwargs.get("label")
        self.value = kwargs.get("value")

        if kwargs.get("alignment") == "left":
            self.alignment = QtCore.Qt.RightToLeft
        else:
            self.alignment = QtCore.Qt.LeftToRight

        self.minimumSize = kwargs.get("minimumSize")
        self.maximumSize = kwargs.get("maximumSize")

        self.horizontalPolicy = (
            QtWidgets.QSizePolicy.Preferred
            if kwargs.get("horizontalPolicy") is None
            else kwargs.get("horizontalPolicy", QtWidgets.QSizePolicy.Preferred)
        )

        self.veritcalPolicy = (
            QtWidgets.QSizePolicy.Preferred
            if kwargs.get("veritcalPolicy") is None
            else kwargs.get("veritcalPolicy", QtWidgets.QSizePolicy.Preferred)
        )

        if self.minimumSize:
            self.setMinimumSize(QtCore.QSize(self.minimumSize, 0))
        if self.maximumSize:
            self.setMaximumSize(QtCore.QSize(self.maximumSize, 16777215))

        sizepolicy = QtWidgets.QSizePolicy(self.horizontalPolicy, self.veritcalPolicy)
        self.setSizePolicy(sizepolicy)

        self.setLayoutDirection(self.alignment)
        self.setText(self.label)
        self.setChecked(self.value)

    def setValue(self, value):
        self.value = value
        self.setChecked(value)

    def value(self):
        return self.value


if __name__ == "__main__":
    pass
