# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, QRunnable(thread) wrapper source code.

from __future__ import absolute_import


import sys
import traceback

from PySide2 import QtCore


class WorkerSignals(QtCore.QObject):
    finished = QtCore.Signal(dict)
    error = QtCore.Signal(dict)
    result = QtCore.Signal(dict)
    progress = QtCore.Signal(dict)


class WorkerImportRunner(QtCore.QRunnable):
    name = "import"

    def __init__(self, fn, *args, **kwargs):
        super(WorkerImportRunner, self).__init__()

        self.fn = fn
        self.filepath = args[0]
        self.displayLogs = args[1]
        self.widget = args[2]
        self.kwargs = kwargs

        self.signals = WorkerSignals()

        self.setAutoDelete(True)

        self.kwargs["logger"] = self.displayLogs
        self.kwargs["progressCallback"] = self.signals.progress

    def run(self):
        try:
            result = self.fn(self.filepath, self.widget, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc(), self.widget))
            result = None
        else:
            context = {"widget": self.widget, "context": result}
            self.signals.result.emit(context)
        finally:
            context = {"widget": self.widget, "context": result}
            self.signals.finished.emit(context)


class WorkerExportRunner(WorkerImportRunner):
    name = "export"


class _WorkerExportRunner(QtCore.QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(WorkerExportRunner, self).__init__()

        self.fn = fn
        self.filepath = args[0]
        self.displayLogs = args[1]
        self.widget = args[2]
        self.kwargs = kwargs

        self.signals = WorkerSignals()

        self.setAutoDelete(True)

        self.kwargs["logger"] = self.displayLogs
        self.kwargs["progressCallback"] = self.signals.progress

    def run(self):
        try:
            result = self.fn(self.filepath, self.widget, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc(), self.widget))
            result = None
        else:
            context = {"widget": self.widget, "result": result}
            self.signals.result.emit(context)
        finally:
            context = {"widget": self.widget, "result": result}
            self.signals.finished.emit(context)


if __name__ == "__main__":
    pass
