# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, QGroupBox wrapper class source code.

from __future__ import absolute_import

from functools import partial

import resources

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import utils
from kore import batch
from kore import thread
from kore import logger
from kore import constant

from widgets.labels import RightLabel
from widgets.labels import InputLable
from widgets.buttons import ClearButton
from widgets.buttons import CacheButton
from widgets.labels import FrameSpinBox
from widgets.labels import NormalComboBox
from widgets.labels import NormalLineEdit
from widgets.labels import CameraCheckBox
from widgets.labels import ProjectLineEdit
from widgets.buttons import CacheSaveButton
from widgets.labels import CacheTypeComboBox
from widgets.buttons import BrowsePathButton
from widgets.labels import CompleterLineEdit
from widgets.labels import LocalPathLineEdit
from widgets.buttons import ProjectSaveButton
from widgets.labels import InputCompleterLineEdit


LOGGER = logger.getLogger(__name__)


class NormalGroup(QtWidgets.QGroupBox):
    def __init__(self, parent, title, **kwargs):
        super(NormalGroup, self).__init__(parent, title)
        self.__parent__ = parent
        self.title = title

        if self.title:
            self.setTitle(self.title)

        self.setFlat(True)

        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        self.setSizePolicy(sizepolicy)


class ProjectGroup(NormalGroup):
    def __init__(self, parent, title, **kwargs):
        super(ProjectGroup, self).__init__(parent, title)

        self.name = "projectSettings"
        self.context = dict()
        self.presetContext = dict()

        self.validExtensions = list()

        self.presetsFilePath = resources.getProjectPresetsPath()
        self.projectContextList = self.getPresetContextList()

        self.gridlayout = QtWidgets.QGridLayout(self)
        self.gridlayout.setHorizontalSpacing(10)
        self.gridlayout.setVerticalSpacing(10)
        self.gridlayout.setContentsMargins(20, 20, 20, 20)

        for context in self.projectContextList:
            label = RightLabel(self, label=context["label"])
            self.gridlayout.addWidget(label, context["index"], 0, 1, 1)

            lineedit = ProjectLineEdit(self)
            lineedit.setContext(context)
            lineedit.setValue(value=None)
            self.gridlayout.addWidget(lineedit, context["index"], 1, 1, 1)

            button = BrowsePathButton(self, widget=lineedit)
            self.gridlayout.addWidget(button, context["index"], 2, 1, 1)

            if context.get("extensions"):
                self.validExtensions.extend(context["extensions"])

        self.projectSaveButton = ProjectSaveButton(self)
        self.gridlayout.addWidget(self.projectSaveButton, len(self.projectContextList), 2, 1, 1)

    def getPresetContextList(self):
        localPresetsContext = utils.readJsonFile(self.presetsFilePath)

        projectContextList = constant.PROJECT_CONTEXT_LIST.copy()

        for context in projectContextList:
            if context["key"] not in localPresetsContext:
                continue
            context["value"] = localPresetsContext[context["key"]]

        return projectContextList

    def hasValid(self):
        projectPath = self.presetContext["projectPath"]
        if not projectPath:
            return False
        return utils.isPath(projectPath)

    def setProject(self):
        if not hasattr(self.__parent__, "cachePropertyPage"):
            return
        self.__parent__.cachePropertyPage.setProject(self.presetContext["projectPath"])


class NormalPage(QtWidgets.QWidget):
    def __init__(self, parent, **kwargs):
        super(NormalPage, self).__init__(parent)
        self.__parent__ = parent


class CachePropertyPage(NormalPage):
    def __init__(self, parent, **kwargs):
        super(CachePropertyPage, self).__init__(parent)

        self.name = "property"
        self.saved = False
        self.context = dict()
        self.widgetItem = None
        self.projectPath = None
        self.displayLogs = False
        self.diaplayMessageBox = False
        self.codeList = [None for _ in range(4)]

        self.gridlayout = QtWidgets.QGridLayout(self)
        self.gridlayout.setHorizontalSpacing(10)
        self.gridlayout.setVerticalSpacing(10)
        self.gridlayout.setContentsMargins(20, 20, 20, 20)

        self.clearButton = ClearButton(self)
        self.gridlayout.addWidget(self.clearButton, 0, 3, 1, 1)

        self.showLabel = InputLable(self, label="Show")
        self.gridlayout.addWidget(self.showLabel, 1, 0, 1, 1)

        self.showLineedit = CompleterLineEdit(
            self,
            key="show",
            editable=False,
            maximumSize=QtCore.QSize(200, 16777215),
            labelWidget=self.showLabel,
        )
        self.showLineedit.setEnabled(False)
        self.gridlayout.addWidget(self.showLineedit, 1, 1, 1, 1)

        self.horizontalSpacer = QtWidgets.QSpacerItem(
            108, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridlayout.addItem(self.horizontalSpacer, 1, 2, 1, 2)

        self.kindLabel = InputLable(self, label="Kind (Optional)")
        self.gridlayout.addWidget(self.kindLabel, 2, 0, 1, 1)

        self.kindLineedit = InputCompleterLineEdit(
            self,
            key="kind",
            index=0,
            editable=True,
            modelList=constant.KINDS,
            maximumSize=QtCore.QSize(200, 16777215),
            labelWidget=self.kindLabel,
        )
        self.gridlayout.addWidget(self.kindLineedit, 2, 1, 1, 1)

        self.sequenceLabel = InputLable(self, label="Sequence")
        self.gridlayout.addWidget(self.sequenceLabel, 3, 0, 1, 1)

        self.sequenceLineedit = InputCompleterLineEdit(
            self,
            key="sequence",
            index=1,
            editable=True,
            modelList=constant.SEQUENCES,
            maximumSize=QtCore.QSize(200, 16777215),
            labelWidget=self.sequenceLabel,
        )
        self.gridlayout.addWidget(self.sequenceLineedit, 3, 1, 1, 1)

        self.shotLabel = InputLable(self, label="Shot")
        self.gridlayout.addWidget(self.shotLabel, 4, 0, 1, 1)

        self.shotLineedit = InputCompleterLineEdit(
            self,
            key="shot",
            index=2,
            editable=True,
            modelList=constant.SHOTS,
            maximumSize=QtCore.QSize(200, 16777215),
            labelWidget=self.shotLabel,
        )
        self.gridlayout.addWidget(self.shotLineedit, 4, 1, 1, 1)

        self.taskLabel = InputLable(self, label="Task")
        self.gridlayout.addWidget(self.taskLabel, 5, 0, 1, 1)

        self.taskLineedit = InputCompleterLineEdit(
            self,
            key="task",
            index=3,
            editable=True,
            default=constant.TASKS[0],
            modelList=constant.TASKS,
            maximumSize=QtCore.QSize(200, 16777215),
            labelWidget=self.taskLabel,
        )
        self.codeList[3] = constant.TASKS[0]
        self.gridlayout.addWidget(self.taskLineedit, 5, 1, 1, 1)

        self.fstartLabel = InputLable(self, label="Frame Start")
        self.gridlayout.addWidget(self.fstartLabel, 6, 0, 1, 1)

        self.fstartSpinBox = FrameSpinBox(
            self,
            key="frameStart",
            editable=True,
            minimum=1,
            maximum=999999999,
            maximumSize=QtCore.QSize(200, 16777215),
            default=constant.DEFAULT_FRAME_START,
            labelWidget=self.fstartLabel,
        )
        self.gridlayout.addWidget(self.fstartSpinBox, 6, 1, 1, 1)

        self.fendLabel = InputLable(self, label="Frame End")
        self.gridlayout.addWidget(self.fendLabel, 7, 0, 1, 1)

        self.fendSpinBox = FrameSpinBox(
            self,
            key="frameEnd",
            editable=True,
            minimum=1,
            maximum=999999999,
            maximumSize=QtCore.QSize(200, 16777215),
            default=constant.DEFAULT_FRAME_END,
            labelWidget=self.fendLabel,
        )
        self.gridlayout.addWidget(self.fendSpinBox, 7, 1, 1, 1)

        self.versionLabel = InputLable(self, label="Version")
        self.gridlayout.addWidget(self.versionLabel, 8, 0, 1, 1)

        self.versionLineedit = CompleterLineEdit(
            self,
            key="version",
            index=4,
            editable=True,
            default=constant.DEFAULT_VERSION,
            maximumSize=QtCore.QSize(200, 16777215),
        )
        self.versionLineedit.setEnabled(True)
        self.gridlayout.addWidget(self.versionLineedit, 8, 1, 1, 1)

        self.cameraLabel = InputLable(self, label="Camera")
        self.gridlayout.addWidget(self.cameraLabel, 9, 0, 1, 1)

        self.cameraCheckBox = CameraCheckBox(
            self,
            label="FBX",
            key="cameraFBX",
            editable=True,
            default=True,
            labelWidget=self.cameraLabel,
        )
        self.gridlayout.addWidget(self.cameraCheckBox, 9, 1, 1, 1)

        self.cacheLabel = InputLable(self, label="Cache Type")
        self.gridlayout.addWidget(self.cacheLabel, 10, 0, 1, 1)

        self.cacheCombobox = CacheTypeComboBox(
            self,
            key="cache",
            editable=True,
            context=constant.CACHE_TYPES,
            labelWidget=self.cacheLabel,
        )
        self.gridlayout.addWidget(self.cacheCombobox, 10, 1, 1, 1)

        self.localpathLabel = InputLable(self, label="Local Path")
        self.gridlayout.addWidget(self.localpathLabel, 11, 0, 1, 1)

        self.localpathLineedit = LocalPathLineEdit(
            self,
            key="localPath",
            editable=True,
            labelWidget=self.localpathLabel,
        )
        self.localpathLineedit.setEnabled(False)
        self.gridlayout.addWidget(self.localpathLineedit, 11, 1, 1, 2)

        self.projectLocationButton = BrowsePathButton(self, widget=self.localpathLineedit)
        self.gridlayout.addWidget(self.projectLocationButton, 11, 3, 1, 1)

        self.cachesaveButton = CacheSaveButton(self)
        self.gridlayout.addWidget(self.cachesaveButton, 12, 3, 1, 1)

        self.cacheButton = CacheButton(self)
        self.cacheButton.clicked.connect(partial(self.cacheIt, diaplayMessageBox=True))
        self.gridlayout.addWidget(self.cacheButton, 13, 1, 1, 2)

        self.inputWidgets = [
            [self.showLineedit, self.showLabel],
            [self.kindLineedit, self.kindLabel],
            [self.sequenceLineedit, self.sequenceLabel],
            [self.shotLineedit, self.shotLabel],
            [self.taskLineedit, self.taskLabel],
            [self.fstartSpinBox, self.fstartLabel],
            [self.fendSpinBox, self.fendLabel],
            [self.versionLineedit, self.versionLabel],
            [self.localpathLineedit, self.localpathLabel],
            [self.cameraCheckBox, self.cameraLabel],
            [self.cacheCombobox, self.cacheLabel],
        ]

    def setProject(self, value):
        self.projectPath = value
        self.showLineedit.setValue(utils.folderName(value))

    def updateVersionPath(self):
        if None in self.codeList[1:]:
            LOGGER.warning("Detected None in the codeList %s" % self.codeList)
            return

        taskPath = utils.pathResolver(
            self.__parent__.projectGroup.presetContext["projectPath"],
            folders=self.codeList,
        )

        nextVersion = utils.nextVersion(taskPath)
        self.versionLineedit.setValue(nextVersion)

        versionPath = utils.pathResolver(
            self.__parent__.projectGroup.presetContext["projectPath"],
            folders=self.codeList + [nextVersion],
        )

        exists, widget_item = self.__parent__.fileTreewidget.localPathExists(
            versionPath, widgetItem=self.widgetItem
        )

        if exists:
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "Already exists, %s\n(%s)" % (versionPath, widget_item.filepath),
                QtWidgets.QMessageBox.Ok,
            )
            self.localpathLineedit.reset()
            return

        self.localpathLineedit.setValue(versionPath)
        self.projectLocationButton.browsepath = versionPath

    def reset(self):
        for widget, label in self.inputWidgets:
            if not widget.hasEditable():
                continue
            widget.reset()

    def setDisplayLogs(self, value):
        self.displayLogs = value

    def setValues(self, context):
        for widget, label in self.inputWidgets:
            if widget.hasEditable():
                widget.reset()
            if widget.key not in context:
                label.setEditColor()
                continue
            widget.setValue(context[widget.key])

    def getValues(self):
        context = dict()

        for lineedit, label in self.inputWidgets:
            context[lineedit.key] = lineedit.getValue()

        return context

    def setWidgetItem(self, widgetItem):
        self.widgetItem = widgetItem

    def cacheIt(self, diaplayMessageBox=False):
        if not self.widgetItem:
            LOGGER.warning("Load the treewidget item (select the item) and try")
            return

        if not self.widgetItem.context:
            LOGGER.warning("Save the property and try")
            return

        if not self.widgetItem.hasChecked():
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "Please check the unchecked items and try!..",
                QtWidgets.QMessageBox.Ok,
            )
            return

        if not self.widgetItem.context.get("save"):
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "Save the current item and try!..",
                QtWidgets.QMessageBox.Ok,
            )
            return

        if not self.localpathLineedit.value:
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "Please set the publish localPath and try!..",
                QtWidgets.QMessageBox.Ok,
            )
            return

        self.diaplayMessageBox = diaplayMessageBox

        self.widgetItem.updateContext()

        inputs = self.widgetItem.context.copy()

        if "filepath" in inputs:
            inputs.pop("filepath")

        inputs.update(self.__parent__.projectGroup.context)  # startupContext

        self.widgetItem.setDisplay(3)  # Caching in progress

        exportPool = thread.WorkerExportRunner(
            self.createCache, self.widgetItem.filepath, self.displayLogs, self.widgetItem, **inputs
        )

        exportPool.signals.progress.connect(self.cacheThreadProgress)
        exportPool.signals.error.connect(self.cacheThreadError)
        exportPool.signals.finished.connect(self.cacheThreadFinished)

        self.__parent__.threadCachePool.start(
            exportPool,
            priority=self.__parent__.priority,  # QtCore.QThread.HighestPriority
        )

    def createCache(self, filepath, *args, **kwargs):
        logger.nextLine()
        LOGGER.info("Started creating caches")
        LOGGER.info("Current priority, %s" % self.__parent__.priority)
        LOGGER.info("Source filepath location, %s" % filepath)

        logger.nextLine()

        LOGGER.info("Input context")
        for k, v in kwargs.items():
            LOGGER.info("%s: %s" % (k, v))

        logger.nextLine()

        self.exportCache = batch.ExportCache()
        context = self.exportCache.doIt(filepath, **kwargs)

        return context

    def cacheThreadProgress(self, result):
        LOGGER.info(result)

    def cacheThreadFinished(self, inputs):
        widget = inputs["widget"]
        context = inputs["context"]

        widget.setThreading(False)

        LOGGER.info("Display logs mode, %s" % self.displayLogs)

        if not context["valid"]:
            message = "Python script snippet failure (%s file subprocess failure)." % widget.name
            valid = False

        elif not context["result"]:
            message = "Batch failure, Unexpected input file or cache process."
            valid = False
        else:
            message = "Caching Succeed,  %s" % context["result"]["localPath"]
            valid = True

        if not valid:
            widget.setDisplay(4)
            if self.diaplayMessageBox:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Critical",
                    message,
                    QtWidgets.QMessageBox.Cancel,
                )

            LOGGER.error(message)
            return

        widget.setContext({"isCached": True}, append=True)

        logger.nextLine()
        LOGGER.info("Result: %s" % widget.context["filepath"])

        for context in context["result"]["outputs"]:
            LOGGER.info("Cache file: %s" % context["filepath"])
            LOGGER.info("Node: %s" % context["node"])
            LOGGER.info("Frame range: {}".format(context["frameRange"]))

        widget.setSelected(False)
        widget.setDisplay(5)

        if self.diaplayMessageBox:
            QtWidgets.QMessageBox.information(
                self,
                "Information",
                message,
                QtWidgets.QMessageBox.Ok,
            )
            return

    def cacheThreadError(self, error):
        exctype, value, traceback, widget = error
        print(exctype)
        print(value)
        print(traceback)
        widget.setDisplay(False)


class SuppertPage(NormalPage):
    def __init__(self, parent, **kwargs):
        super(SuppertPage, self).__init__(parent)


if __name__ == "__main__":
    pass
