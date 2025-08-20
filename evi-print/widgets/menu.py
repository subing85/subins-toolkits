# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)  Resolver QGroupBox wrapper source code.
# WARNING! All changes made in this file will be lost when recompiling UI file!

from __future__ import absolute_import

import resources

from functools import partial

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import utils
from kore import logger
from kore import constants

from widgets.messagebox import DisplayBox

LOGGER = logger.getLogger(__name__)


class NormalMenu(QtWidgets.QMenu):
    name = "evi"
    title = "Evi-Menu"

    def __init__(self, parent, **kwargs):
        super(NormalMenu, self).__init__(parent)

        self.__parent__ = parent

        self.setTearOffEnabled(True)
        self.setTitle(self.title)


class FileMenu(NormalMenu):
    name = "fileEvi"
    title = "    File"

    def __init__(self, parent, **kwargs):
        super(FileMenu, self).__init__(parent)

        self.__parent__ = parent

        self.saveFilepath = None

        self.browsepath = kwargs.get("browsepath") or resources.getProjectPath()

        self.newAction = NewAction(self)
        self.newAction.triggered.connect(self.new)
        self.addAction(self.newAction)

        self.openAction = OpenAction(self)
        self.openAction.triggered.connect(self.open)
        self.addAction(self.openAction)

        self.addSeparator()

        self.saveAsAction = SaveAsAction(self)
        self.saveAsAction.triggered.connect(self.saveAs)
        self.addAction(self.saveAsAction)

        self.saveAction = SaveAction(self)
        self.saveAction.triggered.connect(self.save)
        self.addAction(self.saveAction)

        self.addSeparator()

        self.importAction = ImportAction(self)
        self.importAction.triggered.connect(self.importCSV)
        self.addAction(self.importAction)

        self.addSeparator()

        self.quitAction = QuitAction(self)
        self.quitAction.triggered.connect(self.quit)
        self.addAction(self.quitAction)

    def new(self):
        result = DisplayBox(
            self.__parent__, "Warning", "Save changes to untitled scene?", ["Save", "Cancel"]
        )
        if result.replay == DisplayBox.Cancel:
            return

        if result.replay == DisplayBox.Save:
            if self.saveFilepath:
                self.save()
            else:
                self.saveAs()

        self.__parent__.clearAll()

    def open(self):
        # filepath = "C:/Users/batman/Documents/evi-resolve/project_01/test_001.evie"
        # templateContext, pathContext, contextList = utils.openFile(filepath)
        # valid = self.__parent__.setContextList(templateContext, pathContext, contextList)
        # return

        fileDialog = QtWidgets.QFileDialog(self.__parent__)
        filepath, format = fileDialog.getOpenFileName(
            self.__parent__,
            "Browse your CSV file",
            self.browsepath,
            "evi edit scene (*.%s)" % constants.EVIE_EDIT_SCENE_EXTENSTION,
        )

        if not filepath:
            return

        LOGGER.info("Source filepath, %s" % filepath)

        templateContext, pathContext, contextList = utils.openFile(filepath)

        valid = self.__parent__.setContextList(templateContext, pathContext, contextList)

        if valid:
            self.__parent__.setWindowTitle("%s - ( %s )" % (self.__parent__.title, filepath))
            self.saveFilepath = filepath
            self.browsepath = utils.dirname(filepath)
            LOGGER.info("Succeed, open the file from, %s" % filepath)
        else:
            LOGGER.error("Failed, open the file from, %s" % filepath)

    def saveAs(self):
        valid, filepath = self.deploy("Save As", filepath=None)

        if valid:
            self.__parent__.setWindowTitle("%s - ( %s )" % (self.__parent__.title, filepath))
            self.saveFilepath = filepath
            self.browsepath = utils.dirname(filepath)
            LOGGER.info("Succeed, save the file to, %s" % filepath)
        else:
            LOGGER.error("Failed, save the file to, %s" % filepath)

    def save(self):
        valid, filepath = self.deploy("Save As", filepath=self.saveFilepath)

        if valid:
            LOGGER.info("Succeed, save the file to, %s" % filepath)
        else:
            LOGGER.error("Failed, save the file to, %s" % filepath)

    def deploy(self, typed, filepath=None):
        # filepath = filepath or self.saveFilepath

        if not filepath:
            fileDialog = QtWidgets.QFileDialog(self.__parent__)
            filepath, fileFormat = fileDialog.getSaveFileName(
                self.__parent__,
                typed,
                self.browsepath,
                "evi edit scene (*.%s)" % constants.EVIE_EDIT_SCENE_EXTENSTION,
            )

            if not filepath:
                return

        contextList = self.__parent__.contextList()

        valid = utils.saveFile(contextList, filepath)

        return valid, filepath

    def importCSV(self):
        if not self.__parent__.templateGroup.templateCombobox.hasTemplate:
            DisplayBox(
                self, "Warning", "Please load the template first and try to import CSV file", ["Ok"]
            )
            return

        fileDialog = QtWidgets.QFileDialog(self.__parent__)
        formatPattern = "(*.csv)"
        filepath, format = fileDialog.getOpenFileName(
            self.__parent__, "Browse your CSV file", self.browsepath, formatPattern
        )

        if not filepath:
            return
        self.browsepath = utils.dirname(filepath)

        LOGGER.info("CSV file path, %s %s" % (filepath, format))

        self.__parent__.outlineTreewidget.loadItem(
            utils.pathResolver(filepath),
            self.__parent__.inputGroup.inputContext,
            self.__parent__.barcodeGroup.barcodeContext,
            self.__parent__.fieldGroup.fieldContextList,
        )

    def quit(self, *args):
        result = DisplayBox(
            self.__parent__, "Question", "Are you sure want to close?", ["Yes", "No"]
        )

        if result.replay == DisplayBox.No:
            return

        self.__parent__.close()


class EditMenu(NormalMenu):
    name = "editEvi"
    title = "    Edit"

    def __init__(self, parent, **kwargs):
        super(EditMenu, self).__init__(parent)

        self.__parent__ = parent

        self.modeAction = ModeAction(self)
        self.addAction(self.modeAction)

        self.exportAction = ExportAction(self)
        self.addAction(self.exportAction)

        self.addSeparator()

        self.refreshAction = RefreshAction(self)
        self.addAction(self.refreshAction)

        self.reloadAction = ReloadAction(self)
        self.addAction(self.reloadAction)

        self.addSeparator()

        self.preferenceAction = PreferenceAction(self)
        self.addAction(self.preferenceAction)


class HelpMenu(NormalMenu):
    name = "editEvi"
    title = "    Help"

    def __init__(self, parent, **kwargs):
        super(HelpMenu, self).__init__(parent)

        self.__parent__ = parent

        self.helpAction = HelpAction(self)
        self.addAction(self.helpAction)

        self.helpAction.triggered.connect(self.help)

    def help(self):
        print(self.__parent__.composite.backgroundLayer.filepath)


class NormalAction(QtWidgets.QAction):
    label = "normal"
    icon = "normal"
    toolTip = "normal"

    def __init__(self, parent, **kwargs):
        super(NormalAction, self).__init__(parent)

        self.setText(self.label)
        self.setToolTip(self.toolTip)

        self.iconpath = resources.getIconFilepath(self.icon)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.iconpath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(icon)


class NewAction(NormalAction):
    label = "New"
    icon = "new"
    toolTip = "New scene"


class OpenAction(NormalAction):
    label = "open"
    icon = "open"
    toolTip = "Open the scene"


class SaveAsAction(NormalAction):
    label = "Save As"
    icon = "saveAs"
    toolTip = "Save as the current scene"


class SaveAction(NormalAction):
    label = "Save"
    icon = "save"
    toolTip = "Save the current scene"


class ImportAction(NormalAction):
    label = "Import CSV"
    icon = "import"
    toolTip = "Import the CSV file"


class QuitAction(NormalAction):
    label = "Quit"
    icon = "quit"
    toolTip = "Quit the application"


class RefreshAction(NormalAction):
    label = "Refresh"
    icon = "refresh"
    toolTip = "Refresh based on CSV input"


class ReloadAction(NormalAction):
    label = "Reload"
    icon = "reload"
    toolTip = "Reload to origin based on CSV input"


class ModeAction(NormalAction):
    label = "Template Mode"
    icon = "mode"
    toolTip = "Switch to template mode"


class ExportAction(NormalAction):
    label = "Export Template"
    icon = "exportTemplate"
    toolTip = "Export the template"


class PreferenceAction(NormalAction):
    label = "Preference"
    icon = "preference"
    toolTip = "Application preference settings"


class HelpAction(NormalAction):
    label = "About the Application"
    icon = "help"
    toolTip = "About the Application"


if __name__ == "__main__":
    pass
