# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, QtGui wrapper class source code.


from __future__ import absolute_import

import qdarktheme

import resources

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from kore import utils
from kore import constant


class PixmapIcon(QtGui.QIcon):
    def __init__(self, name, **kwargs):
        super(PixmapIcon, self).__init__()

        pixmap = Pixmap(name)
        self.addPixmap(pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)


class Pixmap(QtGui.QPixmap):
    def __init__(self, name, **kwargs):
        super(Pixmap, self).__init__()

        self.name = name

        if constant.LOAD_FROM_DATA:
            imageData = resources.getIconData(self.name)
            self.loadFromData(imageData)
        else:
            iconpath = resources.getIconFilepath(self.name)
            self.load(iconpath)


class Font(QtGui.QFont):
    def __init__(self, size, **kwargs):
        super(Font, self).__init__()

        family = kwargs.get("family")
        bold = kwargs.get("bold") or False

        self.setPointSize(size)
        self.setBold(bold)

        if family:
            self.setFamily(family)


class SetStylesheet(object):
    def __init__(self, parent, **kwargs):
        super(SetStylesheet, self).__init__()

        theme = kwargs.get("theme") or constant.constant.GUI_THEMES[0]

        parent.setStyleSheet(qdarktheme.load_stylesheet(theme))


class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self, **kwrags):
        super(SplashScreen, self).__init__()

        splashImages = resources.getSplashs()

        splashImage = splashImages[utils.randomNumber(len(splashImages))]

        pixmap = Pixmap(splashImage)
        self.setPixmap(pixmap)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # No window border
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Create an opacity effect for fading
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacityEffect)

        if kwrags.get("opacity"):
            self.opacityEffect.setOpacity(0)

    def fadeOut(self, duration=1000, callback=None):
        # Create a property animation to control the opacity
        fadeAnimation = QtCore.QPropertyAnimation(self.opacityEffect, b"opacity")
        fadeAnimation.setDuration(duration)
        fadeAnimation.setStartValue(1.0)  # Start fully visible
        fadeAnimation.setEndValue(0.0)  # End fully transparent
        fadeAnimation.finished.connect(self.close)  # Close the splash screen when finished

        # If there's a callback (like showing the main window), call it after fade finishes
        if callback:
            fadeAnimation.finished.connect(callback)

        fadeAnimation.start()


if __name__ == "__main__":
    pass
