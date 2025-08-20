# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, QLabel wrapper class source code.


from __future__ import absolute_import

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import utils
from kore import logger
from kore import constant

from widgets import Font
from widgets import Pixmap
from widgets import PixmapIcon

LOGGER = logger.getLogger(__name__)


class TitleLabel(QtWidgets.QLabel):
    def __init__(self, parent, name, **kwargs):
        super(TitleLabel, self).__init__(parent)

        self.__parent__ = parent

        pixmap = Pixmap(name)
        self.setPixmap(pixmap)
        self.setScaledContents(False)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        self.setSizePolicy(sizePolicy)


class CopyrightLabel(QtWidgets.QLabel):
    def __init__(self, parent, **kwargs):
        super(CopyrightLabel, self).__init__(parent)

        self.__parent__ = parent

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        self.setSizePolicy(sizePolicy)

        font = Font(9, family="Arial", bold=True)
        self.setFont(font)

        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.setText(constant.COPYRIGHT_LABEL)


class RightLabel(QtWidgets.QLabel):
    def __init__(self, parent, **kwargs):
        super(RightLabel, self).__init__(parent)

        self.__parent__ = parent

        self.label = kwargs.get("label")

        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.setText(self.label)


class InputLable(RightLabel):
    def __init__(self, parent, **kwargs):
        super(InputLable, self).__init__(parent, **kwargs)

        # self.setStyleSheet("color: rgb(255, 0, 0);")

    def setEditColor(self):
        self.setStyleSheet("color: rgb(255, 0, 0);")

    def setSavedColor(self):
        self.setStyleSheet("")


class NormalLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent, **kwargs):
        super(NormalLineEdit, self).__init__(parent)

        self.__parent__ = parent

        self.key = kwargs.get("key")
        self.index = kwargs.get("index")
        self.editable = kwargs.get("editable", True)
        self.value = None
        self.default = kwargs.get("default")
        self.labelWidget = kwargs.get("labelWidget")

        if kwargs.get("maximumSize"):
            self.setMaximumSize(kwargs["maximumSize"])

        self.setEnabled(self.editable)

    def getValue(self):
        self.value = self.text()
        return self.value

    def hasEditable(self):
        return self.editable

    def reset(self):
        if self.default:
            self.setText(self.default)
            self.value = self.default
        else:
            self.clear()


class CompleterLineEdit(NormalLineEdit):
    def __init__(self, parent, **kwargs):
        super(CompleterLineEdit, self).__init__(parent, **kwargs)

        self.modelList = kwargs.get("modelList") or list()

        self.completerModel = QtCore.QStringListModel(self.modelList)
        self.completer = QtWidgets.QCompleter()
        self.completer.setModel(self.completerModel)
        self.setCompleter(self.completer)

        self.editingFinished.connect(self.lineEditChange)

    def lineEditChange(self, *args):
        newText = self.text()

        self.value = newText

        if self.value not in self.modelList:
            self.modelList.append(self.value)

        self.completerModel.setStringList(self.modelList)

    def setValue(self, value):
        self.value = value

        if not value:
            return

        if isinstance(value, list):
            value = str(value)

        self.setText(value)
        if self.value not in self.modelList:
            self.modelList.append(self.value)

        self.completerModel.setStringList(self.modelList)


class LocalPathLineEdit(CompleterLineEdit):
    def __init__(self, parent, **kwargs):
        super(LocalPathLineEdit, self).__init__(parent, **kwargs)


class ProjectLineEdit(NormalLineEdit):
    def __init__(self, parent, **kwargs):
        super(ProjectLineEdit, self).__init__(parent)

        self.modelList = kwargs.get("modelList") or list()

        self.completerModel = QtCore.QStringListModel(self.modelList)
        self.completer = QtWidgets.QCompleter()
        self.completer.setModel(self.completerModel)
        self.setCompleter(self.completer)

        self.editingFinished.connect(self.lineEditFinished)
        self.textChanged.connect(self.lineEditChange)

    def setContext(self, context, append=False):
        if append:
            self.context.update(context)
        else:
            self.context = context

        self.contextList = list(self.context.values())
        for k, v in context.items():
            setattr(self, k, v)

    def setValue(self, value=None):
        self.value = value or self.context.get("value")

        self.setText(self.value)

        self.lineEditFinished()

    def lineEditFinished(self):
        self.value = self.text()

        self.__parent__.presetContext[self.key] = self.value

        if self.value not in self.modelList:
            self.modelList.append(self.value)

        self.completerModel.setStringList(self.modelList)

    def lineEditChange(self):
        self.value = self.text()
        self.__parent__.presetContext[self.key] = self.value

        if self.key == "projectPath":
            self.__parent__.setProject()


class InputCompleterLineEdit(NormalLineEdit):
    def __init__(self, parent, **kwargs):
        super(InputCompleterLineEdit, self).__init__(parent, **kwargs)

        self.default = kwargs.get("default")
        self.modelList = kwargs.get("modelList") or list()

        self.completerModel = QtCore.QStringListModel(self.modelList)
        self.completer = QtWidgets.QCompleter()
        self.completer.setModel(self.completerModel)
        self.setCompleter(self.completer)

        self.textChanged.connect(self.inputTextChanged)

        if self.default:
            self.setValue(self.default)

    def setValue(self, value):
        self.value = value

        if not value:
            return

        if isinstance(value, list):
            value = str(value)

        self.setText(value)
        if self.value not in self.modelList:
            self.modelList.append(self.value)

        self.completerModel.setStringList(self.modelList)

    def inputTextChanged(self, text):
        if self.value == text:
            self.labelWidget.setSavedColor()
            saved = True

        else:
            self.labelWidget.setEditColor()
            saved = False

        if hasattr(self.__parent__.widgetItem, "context"):
            self.__parent__.widgetItem.context["save"] = saved

        value = text or None

        self.__parent__.codeList[self.index] = value

        self.__parent__.updateVersionPath()


class NormalSpinBox(QtWidgets.QSpinBox):
    def __init__(self, parent, **kwargs):
        super(NormalSpinBox, self).__init__(parent)

        self.__parent__ = parent

        self.default = kwargs.get("default")
        self.key = kwargs.get("key")
        self.editable = kwargs.get("editable", True)
        self.labelWidget = kwargs.get("labelWidget")

        self.currentValue = None

        self.setMinimum(kwargs.get("minimum") or 0)
        self.setMaximum(kwargs.get("maximum") or 999999999)

        if kwargs.get("maximumSize"):
            self.setMaximumSize(kwargs["maximumSize"])

        self.setEnabled(self.editable)
        self.setValue(self.default)

    def getValue(self):
        self.currentValue = self.value()
        return self.currentValue

    def reset(self):
        self.setValue(self.default)

    def hasEditable(self):
        return self.editable


class FrameSpinBox(NormalSpinBox):
    def __init__(self, parent, **kwargs):
        super(FrameSpinBox, self).__init__(parent, **kwargs)

        self.valueChanged.connect(self.frameValueChange)

    def frameValueChange(self, value):
        if self.currentValue == value:
            self.labelWidget.setSavedColor()
            saved = True

        else:
            self.labelWidget.setEditColor()
            saved = False

        if hasattr(self.__parent__.widgetItem, "context"):
            self.__parent__.widgetItem.context["save"] = saved


class NormalCheckBox(QtWidgets.QCheckBox):
    def __init__(self, parent, **kwargs):
        super(NormalCheckBox, self).__init__(parent)

        self.__parent__ = parent

        self.default = kwargs.get("default")
        self.label = kwargs.get("label")
        self.key = kwargs.get("key")
        self.editable = kwargs.get("editable", True)
        self.context = kwargs.get("context")

        self.labelWidget = kwargs.get("labelWidget")

        self.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.setEnabled(self.editable)
        self.setText(self.label)
        self.setChecked(self.default)

    def getValue(self):
        self.value = self.isChecked()
        return self.value

    def setValue(self, value):
        self.value = value
        self.setChecked(value)

    def reset(self):
        self.setChecked(self.default)

    def hasEditable(self):
        return self.editable


class CameraCheckBox(NormalCheckBox):
    def __init__(self, parent, **kwargs):
        super(CameraCheckBox, self).__init__(parent, **kwargs)

        self.stateChanged.connect(self.cameraStateChanged)

    def cameraStateChanged(self, value):
        if self.value == bool(value):
            self.labelWidget.setSavedColor()
            saved = True
        else:
            self.labelWidget.setEditColor()
            saved = False

        if hasattr(self.__parent__.widgetItem, "context"):
            self.__parent__.widgetItem.context["save"] = saved


class NormalComboBox(QtWidgets.QComboBox):
    def __init__(self, parent, **kwargs):
        super(NormalComboBox, self).__init__(parent)

        self.__parent__ = parent

        self.key = kwargs.get("key")
        self.editable = kwargs.get("editable", True)

        self.context = kwargs.get("context")
        self.labelWidget = kwargs.get("labelWidget")
        self.default = 0

        self.value = None
        self.values = list()

    def setValues(self, context):
        context = context or self.context
        self.clear()

        values = list()
        for x in context["values"]:
            if isinstance(x, dict):
                values.append("%s ( %s )" % (x["index"], x["label"]))
            else:
                values = context["values"]
                break

        self.addItems(values)

        self.setCurrentIndex(context["values"].index(context["value"]))
        self.value = context["value"]
        self.values = context["values"]

    def getValue(self):
        self.value = self.currentIndex()
        return self.value

    def setValue(self, index):
        self.value = self.values[index]
        self.setCurrentIndex(index)

    def reset(self):
        self.setCurrentIndex(self.default)

    def hasEditable(self):
        return self.editable


class CacheTypeComboBox(NormalComboBox):
    def __init__(self, parent, **kwargs):
        super(CacheTypeComboBox, self).__init__(parent, **kwargs)

        self.value = None

        self.setValues(self.context)

        self.currentIndexChanged.connect(self.indexChange)

    def indexChange(self, index):
        if self.value == index:
            self.labelWidget.setSavedColor()
            saved = True
        else:
            self.labelWidget.setEditColor()
            saved = False

        if hasattr(self.__parent__.widgetItem, "context"):
            self.__parent__.widgetItem.context["save"] = saved


if __name__ == "__main__":
    pass
