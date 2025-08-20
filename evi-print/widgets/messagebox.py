# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)   Resolver messagebox wrapper source code.
# WARNING! All changes made in this file will be lost when recompiling UI file!

from __future__ import absolute_import

from PySide2 import QtWidgets

from kore import logger

LOGGER = logger.getLogger(__name__)


class DisplayBox(QtWidgets.QMessageBox):
    """Class for adding messageboxes.

    Args:
        typed(str),message(str),buttons(str)
        Maximum of 4 buttons can be given as arguments.

    Returns:
        None

    Examples:
        msgbox = MessageBox("Question", "Do you want to save file?", ["Yes", "No"])
        msgbox = MessageBox(domainTree.parent(), "Critical", stageContext["message"], ["Close"])
    """

    def __init__(self, parent, typed, message, buttons=None, **kwargs):
        super(DisplayBox, self).__init__(parent)

        buttons = buttons or list()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.move(centerPoint)

        msg = []
        for button in buttons:
            if button == "Ok":
                msg.append(QtWidgets.QMessageBox.Ok)
            if button == "Yes":
                msg.append(QtWidgets.QMessageBox.Yes)
            if button == "Save":
                msg.append(QtWidgets.QMessageBox.Save)
            if button == "Cancel":
                msg.append(QtWidgets.QMessageBox.Cancel)
            if button == "Close":
                msg.append(QtWidgets.QMessageBox.Close)
            if button == "Retry":
                msg.append(QtWidgets.QMessageBox.Retry)
            if button == "No":
                msg.append(QtWidgets.QMessageBox.No)

        if typed == "Question":
            self.replay = self.question(self, "Question", message, *msg)

        if typed == "Information":
            self.replay = self.information(self, "Information", message, *msg)

        if typed == "Warning":
            self.replay = self.warning(self, "Warning", message, *msg)

        if typed == "Critical":
            self.replay = self.critical(self, "Critical", message, *msg)


if __name__ == "__main__":
    pass
