# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)  Resolver QComboBox wrapper source code.
# WARNING! All changes made in this file will be lost when recompiling UI file!

from __future__ import absolute_import


from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import utils

# from kore import fonts
from kore import logger
from kore import constants

LOGGER = logger.getLogger(__name__)


class NormalComboBox(QtWidgets.QComboBox):
    def __init__(self, parent, **kwargs):
        super(NormalComboBox, self).__init__(parent)

        self.items = kwargs.get("items") or list()
        self.minimumSize = kwargs.get("minimumSize")
        self.maximumSize = kwargs.get("maximumSize")

        self.setToolTip(kwargs.get("toolTip"))

        if self.minimumSize:
            self.setMinimumSize(QtCore.QSize(self.minimumSize, 0))
        if self.maximumSize:
            self.setMaximumSize(QtCore.QSize(self.maximumSize, 16777215))
        if self.items:
            self.addItems(self.items)

        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        self.setSizePolicy(sizepolicy)

    def setValue(self, index):
        value = index or 0

        if isinstance(value, int):
            value = index
            self.setCurrentIndex(value)

        if isinstance(value, str):
            for x in range(self.count()):
                itemText = self.itemText(x)
                if itemText != value:
                    continue
                value = x
                break
            else:
                value = 0

        self.setCurrentIndex(value)

    def value(self):
        return self.currentText()


class TemplateComboBox(QtWidgets.QComboBox):
    def __init__(self, parent, **kwargs):
        super(TemplateComboBox, self).__init__(parent)

        self.templatePath = kwargs.get("templatePath")
        self.minimumSize = kwargs.get("minimumSize")
        self.maximumSize = kwargs.get("maximumSize")

        self.__parent__ = parent

        self.context = dict()
        self.contextList = list()
        self.hasTemplate = False

        self.setToolTip(kwargs.get("toolTip"))

        if self.minimumSize:
            self.setMinimumSize(QtCore.QSize(self.minimumSize, 0))
        if self.maximumSize:
            self.setMaximumSize(QtCore.QSize(self.maximumSize, 16777215))

        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        self.setSizePolicy(sizepolicy)

        self.currentIndexChanged.connect(self.setCurrentContext)

    def loadAllTemplates(self):
        self.contextList = utils.collectFilesContextList(self.templatePath, "xml", reverse=True)
        self.context = self.contextList[0] if self.contextList else dict()
        self.addItems([context["filename"] for context in self.contextList])

    def setCurrentContext(self, index):
        self.context = self.contextList[index]
        self.loadTemplates()
        LOGGER.info("Current template context, %s" % self.context)

    def loadCurrentContext(self, name):
        context_list = list(filter(lambda x: x["filename"] == name, self.contextList))

        if not context_list:
            return False, "Template missing, could not found ( %s ) template" % name

        index = self.contextList.index(context_list[0])
        self.setCurrentIndex(index)

        return True, "Succeed"

    def clearContext(self):
        self.setCurrentIndex(0)
        self.context = self.contextList[0]
        self.loadTemplates()
        LOGGER.info("Current template context set to ( Null ) context")

    def loadTemplates(self):
        # self.__parent__.__parent__.diagramGroup.layer.clear()
        self.__parent__.__parent__.inputGroup.clear()
        self.__parent__.__parent__.fieldGroup.clear()
        self.__parent__.__parent__.renderGroup.clear()

        if not self.context.get("filepath"):
            self.__parent__.__parent__.outlineTreewidget.clear()
            self.hasTemplate = False
            return

        self.hasTemplate = True

        inputContext, barcodeContext, fieldContextList = utils.importTemplate(
            self.context["filepath"]
        )
        filepath = utils.dirname(self.context["filepath"])

        if self.__parent__.__parent__.hasLoadedOutlineItems:
            for child in self.__parent__.__parent__.outlineTreewidget.children:
                child.inputContext["background"]["default"] = utils.pathResolver(
                    filepath, filename=inputContext["background"]["default"]
                )
                for fieldContext in child.fieldContextList:
                    index = fieldContext["index"]["default"]
                    field_contexts = list(
                        filter(lambda x: x["index"]["default"] == index, fieldContextList)
                    )
                    if not field_contexts:
                        continue
                    for x in fieldContext:
                        fieldContext[x]["default"] = field_contexts[-1][x]["default"]
                        if field_contexts[-1][x].get("value"):
                            fieldContext[x]["value"] = fieldContext[x]["value"]
            if self.__parent__.__parent__.currentOutlineItem:
                field_context_list = self.__parent__.__parent__.currentOutlineItem.fieldContextList
                for fieldContext in fieldContextList:
                    index = fieldContext["index"]["default"]
                    field_contexts = list(
                        filter(lambda x: x["index"]["default"] == index, field_context_list)
                    )
                    if not field_contexts:
                        continue
                    for x in fieldContext:
                        fieldContext[x]["default"] = field_contexts[-1][x]["default"]
                self.__parent__.__parent__.currentOutlineItem.setSelected(False)
        else:
            inputContext["background"]["default"] = utils.pathResolver(
                filepath, filename=inputContext["background"]["default"]
            )
            inputContext["foreground"]["default"] = utils.pathResolver(
                filepath, filename=inputContext["foreground"]["default"]
            )

        # self.__parent__.__parent__.inputGroup.setInputContext(inputContext)
        # self.__parent__.__parent__.barcodeGroup.setBarcodeContext(barcodeContext)

        self.__parent__.__parent__.inputGroup.setValues(inputContext)
        self.__parent__.__parent__.fieldGroup.setValues(fieldContextList)
        self.__parent__.__parent__.barcodeGroup.setValues(barcodeContext)

        # self.__parent__.__parent__.setDiagram()


class FontComboBox(QtWidgets.QFontComboBox):
    def __init__(self, parent, **kwargs):
        super(FontComboBox, self).__init__(parent)

        self.currentFonts = kwargs.get("currentFonts")

        self.minimumSize = kwargs.get("minimumSize")
        self.maximumSize = kwargs.get("maximumSize")

        self.setToolTip(kwargs.get("toolTip"))

        if self.minimumSize:
            self.setMinimumSize(QtCore.QSize(self.minimumSize, 0))
        if self.maximumSize:
            self.setMaximumSize(QtCore.QSize(self.maximumSize, 16777215))

        # self.setFontFilters(QtWidgets.QFontComboBox.ProportionalFonts)

        if self.font:
            self.setCurrentFont(QtGui.QFont(self.currentFonts))

        self.setWritingSystem(QtGui.QFontDatabase.Any)

        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        self.setSizePolicy(sizepolicy)

    def value(self):
        currentFont = self.currentFont()
        return currentFont.family()

        fFamilies = fonts.Families()
        filename = fFamilies.getFilename(currentFont.family())

        return filename

    def setValue(self, value):
        self.currentFonts = value
        self.setCurrentFont(QtGui.QFont(self.currentFonts))


class RenderPageComboBox(QtWidgets.QComboBox):
    def __init__(self, parent, **kwargs):
        super(RenderPageComboBox, self).__init__(parent)

        self.contextList = constants.RENDER_PAGES
        self.currentContext = self.contextList[0]

        items = [x["name"] for x in self.contextList]

        self.addItems(items)

    def value(self):
        index = self.currentIndex()
        currentContext = self.contextList[index]

        return currentContext["name"], currentContext["size"]


class RenderFormatComboBox(QtWidgets.QComboBox):
    def __init__(self, parent, **kwargs):
        super(RenderFormatComboBox, self).__init__(parent)

        self.addItems(constants.RENDER_IMAGE_EXTENSTIONS)

    def value(self):
        return self.currentText()


if __name__ == "__main__":
    pass
