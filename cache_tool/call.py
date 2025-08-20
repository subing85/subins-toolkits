# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, call module.


from __future__ import absolute_import

import os
import sys

from PySide2 import QtCore
from PySide2 import QtWidgets

from widgets import main

from widgets import SplashScreen


def execute(standalone=True):
    if standalone:
        appn = QtWidgets.QApplication(sys.argv)
        splash = SplashScreen()
        splash.show()

    kwargs = {
        "title": "Motion-Craft Cache Tool",
        "wsize": [1500, 1200],
        "titleSize": [1300, 100],
        "maximize": False,
    }
    window = main.MainWindow(parent=None, **kwargs)

    if standalone:
        QtCore.QTimer.singleShot(2000, lambda: splash.fadeOut(1000, window.show()))
    else:
        window.show()

    if standalone:
        sys.exit(appn.exec_())


if __name__ == "__main__":
    execute()
