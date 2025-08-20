# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)  media module.
# WARNING! All changes made in this file will be lost when recompiling UI file!

from __future__ import absolute_import

import io
import barcode

import resources

from PySide2 import QtGui
from PySide2 import QtCore

from kore import utils
from kore import logger
from kore import layers

LOGGER = logger.getLogger(__name__)

IMAGE_FORMAT_MODE = QtGui.QImage.Format_ARGB32


class Composite(object):
    def __init__(self):
        self.backgroundLayer = None
        self.foregroundLayer = None
        self.barcodeLayer = None
        self.textLayers = dict()

        self.baseImage = None
        self.backgroundImage = None
        self.foregroundImage = None
        self.barcodeImage = None
        self.textImages = dict()

        self.foregrounPositionContext = dict()
        self.foregrounPositionRange = dict()

    def addBackgroundLayer(self, layer):
        self.backgroundLayer = layer

    def addForegroundLayer(self, layer):
        self.foregroundLayer = layer

    def addBarcodeLayer(self, layer):
        self.barcodeLayer = layer

    def addTextLayer(self, index, textLayer):
        self.textLayers[index] = textLayer

    def setParameters(self, **kwargs):
        if not self.backgroundLayer:
            LOGGER.warning("Could not found backgroundLayer")
            return

        backgroundImage = self.backgroundLayer.setParameters()

        self.baseImage = QtGui.QImage(backgroundImage.size(), IMAGE_FORMAT_MODE)
        self.baseImage.setDotsPerMeterX(backgroundImage.dotsPerMeterX())
        self.baseImage.setDotsPerMeterY(backgroundImage.dotsPerMeterY())

        self.baseImage.fill(QtCore.Qt.transparent)  # Start with a transparent image

        basePainter = QtGui.QPainter(self.baseImage)
        basePainter.drawImage(QtCore.QPoint(0, 0), backgroundImage)

        if self.foregroundLayer and self.foregroundLayer.isActive:
            foregroundImage = self.foregroundLayer.setParameters(backgroundImage)
            basePainter.drawImage(QtCore.QPoint(0, 0), foregroundImage)
            self.foregrounPositionContext, self.foregrounPositionRange = self.alignment(
                self.baseImage, foregroundImage
            )

        if self.barcodeLayer and self.barcodeLayer.isActive:
            barcodeImage = self.barcodeLayer.setParameters(backgroundImage)
            basePainter.drawImage(QtCore.QPoint(0, 0), barcodeImage)

        for index, textLayer in self.textLayers.items():
            textLayer = textLayer.setParameters(backgroundImage)
            basePainter.drawImage(QtCore.QPoint(0, 0), textLayer)

        # Complete the painting process
        basePainter.end()

        return QtGui.QPixmap.fromImage(self.baseImage)

    def alignment(self, backgroundImage, secondImage):
        bwidth, bheight = backgroundImage.width(), backgroundImage.height()
        fwidth, fheight = secondImage.width(), secondImage.height()

        positionRange = {"x": [(0 - fwidth), (bwidth)], "y": [(0 - fheight), (bheight)]}

        return None, positionRange

        directionContext = {
            "left": {"x": 0, "y": 0},
            "center": {"x": abs(int(bwidth / 2) - int(fwidth / 2)), "y": 0},
            "right": {"x": abs(bwidth - fwidth), "y": 0},
            "top": {"x": 0, "y": 0},
            "middle": {"x": 0, "y": abs(int(bheight / 2) - int(fheight / 2))},
            "bottom": {"x": 0, "y": abs(bheight - fheight)},
        }
        return directionContext, positionRange

    def create(self, inputContext, barcodeContext, fieldContextList):
        backgroundLayer = layers.BackgroundLayer()
        foregroundLayer = layers.ForegroundLayer()
        barcodeLayer = layers.BarcodeLayer()

        self.addBackgroundLayer(backgroundLayer)
        self.addForegroundLayer(foregroundLayer)
        self.addBarcodeLayer(barcodeLayer)

        input_context = dict()
        for k, context in inputContext.items():
            currentValue = context["value"] if "value" in context else context["default"]
            input_context[k] = currentValue

        barcode_context = dict()
        for k, context in barcodeContext.items():
            currentValue = context["value"] if "value" in context else context["default"]
            barcode_context[k] = currentValue

        backgroundLayer.setContext(**input_context)
        backgroundLayer.setActive(True)

        foregroundLayer.setContext(**input_context)
        foregroundLayer.setActive(True)

        barcodeLayer.setContext(**barcode_context)
        barcodeLayer.setActive(True)

        for index, fieldContext in enumerate(fieldContextList):
            field_context = dict()
            for k, context in fieldContext.items():
                currentValue = context["value"] if "value" in context else context["default"]
                field_context[k] = currentValue

            textLayer = layers.TextLayer(index)
            self.addTextLayer(index, textLayer)
            textLayer.setContext(**field_context)
            textLayer.setActive(True)

        self.setParameters()

        return self.baseImage


class Render(object):
    def __init__(self, backgroundFilepath, contextList, **kwargs):
        self.backgroundFilepath = backgroundFilepath
        self.contextList = contextList

        self.directory = kwargs.get("directory")
        self.prefix = kwargs.get("prefix")
        self.pageName, self.pageSize = kwargs.get("page")
        self.format = kwargs.get("format")
        self.progressBar = kwargs.get("progressBar")

    def execute(self):
        if not utils.hasPathExists(self.directory):
            utils.makedirs(self.directory)

        composite = Composite()

        if self.progressBar:
            self.progressBar.show()
            self.progressBar.setMaximum(len(self.contextList))
            self.progressBar.setValues(0, "Render begins")

        logger.nextLine()
        LOGGER.info("Render begins")

        # =============================================================================================================================================
        # if self.pageSize:
        #     backgroundImage = QtGui.QImage(self.backgroundFilepath).convertToFormat(IMAGE_FORMAT_MODE)
        #     dotsPerMeters = backgroundImage.dotsPerMeterX(),  backgroundImage.dotsPerMeterY()
        #     layoutLayer = layers.LayoutLayer(self.pageSize, dotsPerMeters, backgroundImage.size())
        #     layoutLayer.create()
        # =============================================================================================================================================

        for index, context in enumerate(self.contextList):
            padding = str(context["index"]).zfill(5)

            filename = "%s.%s-%s.png" % (
                padding,
                context["treeContext"]["name"],
                context["treeContext"]["id"],
            )
            filepath = utils.pathResolver(self.directory, filename=filename)

            baseLayer = composite.create(
                context["inputContext"], context["barcodeContext"], context["fieldContextList"]
            )

            baseLayer.save(filepath, "PNG", quality=100)

            # layoutLayer.add()

            if self.progressBar:
                self.progressBar.setValues(index, "Render In progress")

            LOGGER.info("Render, %s" % filepath)
            logger.nextLine()

        if self.progressBar:
            self.progressBar.setValues(100, "Render completed")
            self.progressBar.hide()

        logger.nextLine()
        LOGGER.info("Render completed")
        LOGGER.info("Output path, %s" % utils.dirname(filepath))
        logger.nextLine()


if __name__ == "__main__":
    path = "C:/Users/batman/Documents/evi-resolve/templates/test-0001-background.png"

    rnd = Render(path, [])

    rnd.backgroundImage()
