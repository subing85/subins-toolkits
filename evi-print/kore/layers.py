# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works ID - Card  Resolver fonts object.
# WARNING! All changes made in this file will be lost when recompiling UI file!

from __future__ import absolute_import

import io
import barcode

from kore import utils
from kore import logger

from PySide2 import QtGui
from PySide2 import QtCore

LOGGER = logger.getLogger(__name__)
IMAGE_FORMAT_MODE = QtGui.QImage.Format_ARGB32


class NormalLayer(object):
    def __init__(self, *args, **kwargs):
        self.isActive = False
        self.filepath = None
        self.context = dict()

        self.resolution = None
        self.backgroundImage = None

    def imagePPI(self, image):
        # Get the horizontal and vertical resolution in dots per meter
        dpi_x = image.dotsPerMeterX()
        dpi_y = image.dotsPerMeterY()

        # Convert dots per meter to PPI (Pixels Per Inch)
        ppi_x = dpi_x * 0.0254  # 1 meter = 39.3701 inches, so 1 dot/meter = 0.0254 dots/inch
        ppi_y = dpi_y * 0.0254

        return ppi_x, ppi_y

    def setActive(self, value):
        self.isActive = value

    def imageMaskSize(self, image, value):  # Final #######################
        if self.shape == "rectangle":
            x, y = value, value
            width, height = image.width() - (x * 2), image.height() - (y * 2)
            size = QtCore.QRect(x, y, width, height)

            return size

        # circle
        min_dimension = min(image.width(), image.height())
        max_dimension = max(image.width(), image.height())

        minLimit, maxLimit = self.limits(image)

        if value in range(0, minLimit):
            x, y = 0, 0
            width, height = image.width(), image.height()

        elif value in range(minLimit, maxLimit):
            if image.width() < image.height():
                x, y = 0, value - minLimit
                width, height = image.width(), image.height() - (y * 2)

            else:  # if image.width() > image.height():
                x, y = value - minLimit, 0
                width, height = image.width() - (x * 2), image.height()
        else:
            if image.width() < image.height():
                x, y = value - maxLimit, value - minLimit
                width, height = image.width() - (x * 2), image.height() - (y * 2)

            else:  # if image.width() > image.height():
                x, y = value - minLimit, value - maxLimit
                width, height = image.width() - (x * 2), image.height() - (y * 2)

        size = QtCore.QRect(x, y, width, height)

        return size

    def limits(self, image):
        min_dimension = min(image.width(), image.height())
        max_dimension = max(image.width(), image.height())

        return int(min_dimension / 2), int(max_dimension / 2)

    def maskMaxRange(self, secondImage):
        min_dimension = min(secondImage.width(), secondImage.height())
        maxValue = int(min_dimension / 2)
        # maxValue = (self.foregroundLayer.width() / 2) + (self.foregroundLayer.height() / 2)
        return [0, maxValue]

    def alignments(self, baseImage, secondImage, x, y):
        bwidth, bheight = baseImage.width(), baseImage.height()
        fwidth, fheight = secondImage.width(), secondImage.height()

        directionContext = {
            "left": {"x": 0, "y": y},
            "center": {"x": abs(int(bwidth / 2) - int(fwidth / 2)), "y": y},
            "right": {"x": abs(bwidth - fwidth), "y": y},
            "top": {"x": x, "y": 0},
            "middle": {"x": x, "y": abs(int(bheight / 2) - int(fheight / 2))},
            "bottom": {"x": x, "y": abs(bheight - fheight)},
        }

        return directionContext

    def positionRange(self, baseImage, secondImage):
        bwidth, bheight = baseImage.width(), baseImage.height()
        fwidth, fheight = secondImage.width(), secondImage.height()

        posRange = {"x": [(0 - fwidth), (bwidth)], "y": [(0 - fheight), (bheight)]}

        return posRange


class BackgroundLayer(NormalLayer):
    def __init__(self, *args, **kwargs):
        super(BackgroundLayer, self).__init__()

    def setContext(self, **context):
        self.filepath = context.get("background") or self.context.get("background")
        self.context = context

    def setParameters(self):
        self.backgroundImage = QtGui.QImage(self.filepath).convertToFormat(IMAGE_FORMAT_MODE)

        ppiX, ppiY = self.imagePPI(self.backgroundImage)

        self.dpi = ppiX, ppiY
        self.resolution = round(ppiX)

        self.widthInInches = round(self.backgroundImage.width() / ppiX, 3)
        self.heightInInches = round(self.backgroundImage.height() / ppiY, 3)

        LOGGER.info("Background ppi ( %s %s )" % (ppiX, ppiY))
        LOGGER.info(
            "Background size in inches ( %s x %s )" % (self.widthInInches, self.heightInInches)
        )

        return self.backgroundImage


class ForegroundLayer(NormalLayer):
    def __init__(self, *args, **kwargs):
        super(ForegroundLayer, self).__init__()

    def setContext(self, **context):
        self.context.update(context)

        self.filepath = context.get("foreground") or self.context.get("foreground")
        self.x = context.get("x") or self.context.get("x") or 0
        self.y = context.get("y") or self.context.get("y") or 0

        self.scale = context.get("scale") or self.context.get("scale") or 100
        self.mask = context.get("mask") or self.context.get("mask") or 0
        self.shape = context.get("shape") or self.context.get("shape") or "rectangle"
        self.stroke = context.get("stroke") or self.context.get("stroke") or 10
        self.color = context.get("color") or self.context.get("color") or "#000000"

    def setParameters(self, backgroundImage):
        self.backgroundImage = backgroundImage

        layer = QtGui.QImage(backgroundImage.size(), QtGui.QImage.Format_ARGB32)
        layer.setDotsPerMeterX(backgroundImage.dotsPerMeterX())
        layer.setDotsPerMeterY(backgroundImage.dotsPerMeterY())

        # setDotsPerInchX

        layer.fill(QtCore.Qt.transparent)  # Start with a transparent image

        self.foregroundImage = QtGui.QImage(self.filepath).convertToFormat(IMAGE_FORMAT_MODE)
        self.foregroundInstanceImage = QtGui.QImage(self.filepath).convertToFormat(
            IMAGE_FORMAT_MODE
        )

        if self.foregroundInstanceImage.width() < self.foregroundInstanceImage.height():
            self.foregroundImage = self.foregroundInstanceImage.scaledToWidth(
                (self.foregroundInstanceImage.width() * (self.scale / 100)),
                mode=QtCore.Qt.SmoothTransformation,
            )
        else:
            self.foregroundImage = self.foregroundInstanceImage.scaledToWidth(
                (self.foregroundInstanceImage.height() * (self.scale / 100)),
                mode=QtCore.Qt.SmoothTransformation,
            )

        ppiX, ppiY = self.imagePPI(self.foregroundImage)

        self.dpi = ppiX, ppiY
        self.resolution = round(ppiX)

        self.widthInInches = round(self.foregroundImage.width() / ppiX, 3)
        self.heightInInches = round(self.foregroundImage.height() / ppiY, 3)

        LOGGER.info("Foreground ppi ( %s %s )" % (ppiX, ppiY))
        LOGGER.info(
            "Foreground size in inches ( %s x %s )" % (self.widthInInches, self.heightInInches)
        )

        # Set foreground mask
        self.maskImage = QtGui.QImage(self.foregroundImage.size(), QtGui.QImage.Format_ARGB32)
        self.maskImage.fill(QtCore.Qt.transparent)

        qMaskRectSize = self.imageMaskSize(self.foregroundImage, self.mask)

        maskPainterPath = QtGui.QPainterPath()
        if self.shape == "circle":
            maskPainterPath.addRoundedRect(
                qMaskRectSize, self.mask, self.mask, QtCore.Qt.AbsoluteSize
            )
        else:
            maskPainterPath.addRect(qMaskRectSize)

        maskPainter = QtGui.QPainter(self.maskImage)
        maskPainter.setClipPath(maskPainterPath)

        maskPainter.drawImage(0, 0, self.foregroundImage)

        if self.stroke:
            self.strokeImage = QtGui.QImage(self.foregroundImage.size(), QtGui.QImage.Format_ARGB32)
            self.strokeImage.fill(QtCore.Qt.transparent)  # Start with a transparent image

            strokePainter = QtGui.QPainter(self.strokeImage)
            strokePainter.setRenderHint(QtGui.QPainter.Antialiasing)

            # Define the pen to create the outline (similar to 'width' in Pillow)
            strokePen = QtGui.QPen(QtGui.QColor(self.color))
            strokePen.setWidth(self.stroke)
            strokePainter.setPen(strokePen)

            if self.shape == "circle":
                # Draw the rounded rectangle (similar to `draw.rounded_rectangle` in Pillow)
                strokePainter.drawRoundedRect(
                    qMaskRectSize, self.mask, self.mask
                )  # 10 is the radius for rounded corners
            else:
                strokePainter.drawRect(qMaskRectSize)

            strokePainter.end()

            maskPainter.drawImage(0, 0, self.strokeImage)

        maskPainter.end()

        basePainter = QtGui.QPainter(layer)
        # basePainter.drawImage(QtCore.QPoint(self.x, self.y), self.foregroundImage)
        basePainter.drawImage(QtCore.QPoint(self.x, self.y), self.maskImage)

        # Complete the painting process
        basePainter.end()

        return layer

    def getAlignments(self):
        result = self.alignments(self.backgroundImage, self.foregroundImage, self.x, self.y)
        return result

    def getPositionRange(self):
        result = self.positionRange(self.backgroundImage, self.foregroundImage)
        return result

    def getMaskMaxRange(self):
        result = self.maskMaxRange(self.foregroundImage)

        return self.mask, result


class BarcodeLayer(NormalLayer):
    def __init__(self, *args, **kwargs):
        super(BarcodeLayer, self).__init__()

    def setContext(self, **context):
        self.text = context.get("text")

        self.x = context.get("x") or 0
        self.y = context.get("y") or 0

        self.format = context.get("format") or "PNG"

        self.scale = context.get("scale") or 100

        if self.scale > 99:
            self.width, self.height = utils.aspectScale(0.2, 10.0, self.scale)
        else:
            self.width, self.height = 0.2, 10.0

        # self.width, self.height  = 0.2, 10.0

        self.fontSize = context.get("fontSize") or 7  # 10
        self.textDistance = context.get("textDistance") or 3  # 5.0
        self.quietZone = context.get("quietZone") or 6.5
        self.dpi = context.get("dpi") or 143  # 300

        self.background = context.get("background") or "white"
        self.foreground = context.get("foreground") or "black"

        self.context = context

    def setParameters(self, backgroundImage):
        self.backgroundImage = backgroundImage

        if self.text:
            codex = barcode.codex.Code128(self.text, writer=barcode.writer.ImageWriter())

            barcodeImageStream = io.BytesIO()

            codex.write(
                barcodeImageStream,
                options={
                    "format": self.format,
                    "module_width": self.width,
                    "module_height": self.height,
                    "font_size": self.fontSize,
                    "text_distance": self.textDistance,
                    "quiet_zone": self.quietZone,
                    "dpi": self.dpi,
                    "background": self.background,
                    "foreground": self.foreground,
                },
            )

            barcodeImageStream.seek(0)

            self.barcodeImage = QtGui.QImage()
            self.barcodeImage.loadFromData(barcodeImageStream.read())
            self.barcodeImage.convertToFormat(IMAGE_FORMAT_MODE)
        else:
            self.barcodeImage = None

        if self.scale < 100:
            if self.barcodeImage.width() < self.barcodeImage.height():
                self.barcodeImage = self.barcodeImage.scaledToWidth(
                    (self.barcodeImage.height() * (self.scale / 100)),
                    mode=QtCore.Qt.SmoothTransformation,
                )
            else:
                self.barcodeImage = self.barcodeImage.scaledToWidth(
                    (self.barcodeImage.width() * (self.scale / 100)),
                    mode=QtCore.Qt.SmoothTransformation,
                )

        layer = QtGui.QImage(self.backgroundImage.size(), QtGui.QImage.Format_ARGB32)
        layer.fill(QtCore.Qt.transparent)  # Start with a transparent image

        if self.barcodeImage:
            barcodePainter = QtGui.QPainter(layer)
            barcodePainter.setRenderHint(QtGui.QPainter.Antialiasing)

            barcodePainter.drawImage(QtCore.QPoint(self.x, self.y), self.barcodeImage)

            barcodePainter.end()

        return layer

    def getAlignments(self):
        result = self.alignments(self.backgroundImage, self.barcodeImage, self.x, self.y)
        return result

    def getPositionRange(self):
        result = self.positionRange(self.backgroundImage, self.barcodeImage)
        return result


class TextLayer(NormalLayer):
    def __init__(self, *args, **kwargs):
        self.index = args[0]
        self.context = dict()

    def setContext(self, **context):
        self.text = context.get("text") or str()
        self.formattedText = self.text.replace("\\n", "\n")

        self.size = context.get("size") or 12
        self.family = context.get("family") or "Times New Roman"

        self.fillColor = context.get("fillColor") or "#000000"  # (0, 0, 0)
        self.x = context.get("x") or 0
        self.y = context.get("y") or 0

        self.bold = bool(context.get("bold"))
        self.italic = bool(context.get("italic"))
        self.spacing = context.get("spacing") or 0

        self.underline = bool(context.get("underline"))
        self.overline = bool(context.get("overline"))
        self.strikeOut = bool(context.get("strikeOut"))

        self.wordSpacing = context.get("wordSpacing") or 0
        self.stretch = context.get("stretch") or 0

        self.stroke = context.get("stroke") or 0
        self.strokeColor = context.get("strokeColor") or "#ffffff"  # (255, 255, 255)

        self.capitalization = context.get("capitalization") or "mixedCase"

        self.context = context

    def setParameters(self, backgroundImage):
        """
        self.text = text
        self.formattedText = text.replace("\\n", "\n")
        self.size = kwargs.get("size") or 12
        self.family = kwargs.get("family") or "Times New Roman"
        self.fillColor = kwargs.get("fillColor") or (0, 0, 0)
        self.x = kwargs.get("x") or 0
        self.y = kwargs.get("y") or 0
        self.bold = bool(kwargs.get("bold"))
        self.italic = bool(kwargs.get("italic"))
        self.spacing = kwargs.get("spacing") or 0
        self.underline = bool(kwargs.get("underline"))
        self.overline = bool(kwargs.get("overline"))
        self.strikeOut = bool(kwargs.get("strikeOut"))
        self.wordSpacing = kwargs.get("wordSpacing") or 0
        self.stretch = kwargs.get("stretch") or 0
        self.stroke = kwargs.get("stroke") or 0
        self.strokeColor = kwargs.get("strokeColor") or (255, 255, 255)
        self.capitalization = kwargs.get("capitalization") or "mixedCase"
        """

        self.backgroundImage = backgroundImage

        self.capitalizationContext = {
            "mixedCase": QtGui.QFont.MixedCase,  # 0 This is the normal text rendering option where no capitalization change is applied.
            "allUppercase": QtGui.QFont.AllUppercase,  # 1 his alters the text to be rendered in all uppercase type.
            "allLowercase": QtGui.QFont.AllLowercase,  # 2 This alters the text to be rendered in all lowercase type.
            "smallCaps": QtGui.QFont.SmallCaps,  # 3 This alters the text to be rendered in small-caps type.
            "capitalize": QtGui.QFont.Capitalize,  # 4 This alters the text to be rendered with the first character of each word as an uppercase character.
        }

        self.currentFont = QtGui.QFont()
        self.currentFont.setPointSizeF(self.size)
        self.currentFont.setFamily(self.family)
        self.currentFont.setBold(self.bold)
        self.currentFont.setItalic(self.italic)
        self.currentFont.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, self.spacing)

        self.currentFont.setUnderline(self.underline)
        self.currentFont.setOverline(self.overline)
        self.currentFont.setStrikeOut(self.strikeOut)

        self.currentFont.setWordSpacing(self.wordSpacing)
        self.currentFont.setStretch(self.stretch)

        self.currentFont.setCapitalization(self.capitalizationContext[self.capitalization])

        self.textPosition = QtCore.QPoint(self.x, self.y)

        self.fill_color = QtGui.QColor(self.fillColor)
        self.stroke_color = QtGui.QColor(self.strokeColor)

        fontMetrics = QtGui.QFontMetrics(self.currentFont)
        self.textBoundingBox = fontMetrics.boundingRect(self.formattedText)

        self.boundingBox = QtCore.QRect(
            self.x, self.y, self.textBoundingBox.width(), self.textBoundingBox.height()
        )

        # self.textLayer = QtGui.QImage(self.foregroundLayer.size(), QtGui.QImage.Format_ARGB32)
        # self.textLayer.fill(QtCore.Qt.transparent)  # Start with a transparent image

        layer = QtGui.QImage(backgroundImage.size(), QtGui.QImage.Format_ARGB32)
        layer.setDotsPerMeterX(backgroundImage.dotsPerMeterX())
        layer.setDotsPerMeterY(backgroundImage.dotsPerMeterY())
        layer.fill(QtCore.Qt.transparent)  # Start with a transparent image

        textPainter = QtGui.QPainter(layer)
        textPainter.setRenderHint(QtGui.QPainter.Antialiasing)
        textPainter.setFont(self.currentFont)

        painterPath = QtGui.QPainterPath()
        painterPath.addText(self.textPosition, self.currentFont, self.formattedText)

        if self.stroke:
            textPainter.strokePath(painterPath, QtGui.QPen(self.stroke_color, self.stroke))

        textPainter.fillPath(painterPath, self.fill_color)

        textPainter.end()

        return layer

    def getAlignments(self):
        result = self.alignments(self.backgroundImage, self.boundingBox, self.x, self.y)
        return result

    def getPositionRange(self):
        result = self.positionRange(self.backgroundImage, self.boundingBox)
        return result


class LayoutLayer(object):
    def __init__(self, size, dpi, cardSize):
        super(LayoutLayer, self).__init__()

        self.size = QtCore.QSize(size[0], size[1])
        self.dpiX, self.dpiY = dpi
        self.cardSize = cardSize

        self.verticalIndex = 0
        self.horizontalIndex = 0

        print(self.size)
        print(self.dpiX)
        print(self.cardSize)

        self.verticalNum = int(self.size.width() / self.cardSize[0])
        self.horizontalNum = int(self.size.height() / self.cardSize[0])

    def create(self):
        layer = QtGui.QImage(self.size, QtGui.QImage.Format_ARGB32)
        layer.setDotsPerMeterX(self.dpiX)
        layer.setDotsPerMeterY(self.dpiY)

        self.basePainter = QtGui.QPainter(layer)

        return self.basePainter

    def add(self, image):
        self.basePainter.drawImage(QtCore.QPoint(self.x, self.y), image)
        self.verticalIndex += 1
        self.horizontalIndex += 1


if __name__ == "__main__":
    background = "C:/Users/batman/Documents/evi-resolve/test/background.png"

    backgroundImage = QtGui.QImage(background).convertToFormat(IMAGE_FORMAT_MODE)
    dotsPerMeters = backgroundImage.dotsPerMeterX(), backgroundImage.dotsPerMeterY()

    pageName, pageSize = "A3", [3508, 4961]

    layoutLayer = LayoutLayer(
        pageSize, dotsPerMeters, (backgroundImage.width(), backgroundImage.height())
    )
    layoutLayer.create()
