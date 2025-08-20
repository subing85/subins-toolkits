# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)  media module.
# WARNING! All changes made in this file will be lost when recompiling UI file!

import os

try:
    from PIL import Image
    from PIL import ImageOps
    from PIL import ImageDraw
    from PIL import ImageFont
except:
    pass

from PySide2 import QtGui

from kore import utils


class Layer(object):
    def __init__(self):
        self.mode = "RGBA"
        self.baseLayer = None
        self.backgroundLayer = None
        self.foregroundLayer = None
        self.foregroundInstanceLayer = None

        self.backgroundFilepath = None
        self.foregroundFilepath = None

        self.x = 0
        self.y = 0
        self.scale = 100
        self.mask = 0
        self.stroke = 0
        self.color = None

        self.test = False

        None,  # "ltr", # "ttb", #  "rtl" (right to left), "ltr" (left to right) or "ttb"  (top to bottom). Requires libraqm.

        # =============================================================================================================================================
        #
        # self.stroke = 0
        # self.color = None
        # self.maskX, self.maskY = 0, 0
        # self.maskX1, self.maskY1 = None, None
        # self.fontValue = None
        # self.fontSize = 12
        # self.fontFamily = "arial"
        # self.fontType = "normal"
        # self.fontColor = (0, 0, 0)
        # self.fontX = 0
        # self.fontY = 0
        # =============================================================================================================================================

        self.context = dict()
        self.textLayers = dict()
        # self.textLayers = list()

    def clear(self):
        self.x = 0
        self.y = 0
        self.scale = 100
        self.mask = 0
        self.stroke = 0
        self.color = None
        self.maskX1, self.maskY1 = None, None

        self.context = dict()

        self.backgroundLayer = None
        self.backgroundFilepath = None
        self.baseLayer = None
        self.foregroundLayer = None

        self.foregroundFilepath = None
        self.foregroundInstanceLayer = None

        self.strokeLayer = None

        self.textLayers = dict()
        self.textLayerContext = dict()

    def setContext(self, context):
        self.context.update(context)
        for k, v in context.items():
            # print("\t", k, v)
            setattr(self, k, v)

    def alignment(self, direction, **kwargs):
        bwidth, bheight = self.backgroundLayer.size
        fwidth, fheight = self.foregroundInstanceLayer.size

        positionRange = {"x": [(0 - fwidth), (bwidth)], "y": [(0 - fheight), (bheight)]}

        directionContext = {
            "left": {"x": 0, "y": self.y},
            "center": {"x": abs(int(bwidth / 2) - int(fwidth / 2)), "y": self.y},
            "right": {"x": abs(bwidth - fwidth), "y": self.y},
            "top": {"x": self.x, "y": 0},
            "middle": {"x": self.x, "y": abs(int(bheight / 2) - int(fheight / 2))},
            "bottom": {"x": self.x, "y": abs(bheight - fheight)},
        }
        position = directionContext[direction]

        return position, positionRange

    def masks(self):
        maxValue = (self.foregroundLayer.width / 2) + (self.foregroundLayer.height / 2)
        return self.mask, [0, maxValue]

    def composition(self, background, forground=None):
        self.backgroundLayer = Image.open(background)  # .convert("RGB")

        if not self.backgroundLayer.info.get("dpi"):
            raise Exception("Invalid image, could not able to get background image dpi (pixels)")

        self.backgroundFilepath = background
        self.backgroundLayer.filepath = background
        self.backgroundLayer.dpi = self.backgroundLayer.info["dpi"]
        self.backgroundLayer.widthInInches = round(
            self.backgroundLayer.width / self.backgroundLayer.dpi[0], 3
        )
        self.backgroundLayer.heightInInches = round(
            self.backgroundLayer.height / self.backgroundLayer.dpi[1], 3
        )

        self.baseLayer = Image.new("RGBA", self.backgroundLayer.size, (255, 255, 255, 0))

        self.baseLayer.paste(self.backgroundLayer, (0, 0), mask=self.backgroundLayer.split()[-1])

        if forground:
            self.foregroundInstanceLayer = Image.open(forground).convert("RGBA")
            self.foregroundInstanceLayer.dpi = self.foregroundInstanceLayer.info["dpi"]

            self.foregroundLayer = self.foregroundInstanceLayer.copy()

            if not self.foregroundLayer.info.get("dpi"):
                raise Exception(
                    "Invalid image, could not able to get foreground image dpi (pixels)"
                )

            self.foregroundFilepath = forground
            self.foregroundLayer.filepath = forground
            self.foregroundLayer.dpi = self.foregroundLayer.info["dpi"]
            self.foregroundLayer.widthInInches = (
                self.foregroundLayer.width / self.foregroundLayer.dpi[0]
            )
            self.foregroundLayer.heightInInches = (
                self.foregroundLayer.height / self.foregroundLayer.dpi[1]
            )

            self.maskX1, self.maskY1 = self.foregroundLayer.size

            self.baseLayer.paste(
                self.foregroundLayer, (0, 0), mask=self.foregroundLayer.split()[-1]
            )

        # self.baseLayer.paste(self.textImageLayer, (0, 0), mask=self.textImageLayer.split()[-1])

        return self.baseLayer.toqpixmap()

    def setDefault(self, filepath):
        pixmap = self.composition(filepath, forground=None)
        return pixmap

    def setBackground(self, filepath):
        pixmap = self.composition(filepath, forground=None)
        return pixmap

    def addForeground(self, filepath):
        pixmap = self.composition(self.backgroundFilepath, forground=filepath)
        return pixmap

    def addStrokeLayer(self, color):
        foregroundAlpha = self.foregroundLayer.split()[-1]
        grayscale = ImageOps.grayscale(self.foregroundLayer)
        self.strokeLayer = ImageOps.colorize(grayscale, black=color, white=color)
        self.strokeLayer.putalpha(foregroundAlpha)
        return self.strokeLayer.toqpixmap()

    def addTextLayer(self, index):
        textLayer = Image.new("RGBA", self.backgroundLayer.size, (255, 255, 255, 0))
        textIdraw = ImageDraw.Draw(textLayer)
        return textLayer

    def setDiagram(self, **kwargs):
        self.x = self.x if kwargs.get("x") is None else kwargs["x"]
        self.y = self.y if kwargs.get("y") is None else kwargs["y"]

        self.scale = self.scale if kwargs.get("scale") is None else kwargs["scale"]
        self.mask = self.mask if kwargs.get("mask") is None else kwargs["mask"]
        self.stroke = self.stroke if kwargs.get("stroke") is None else kwargs["stroke"]

        self.color = kwargs.get("color") or self.color

        textLayerContext = kwargs.get("textLayerContext")

        self.composition(self.backgroundFilepath, forground=None)

        if not self.foregroundInstanceLayer:
            return

        size = (
            int(self.foregroundInstanceLayer.width * (self.scale / 100)),
            int(self.foregroundInstanceLayer.height * (self.scale / 100)),
        )

        foreground_instance_layer = self.foregroundInstanceLayer.copy()

        self.foregroundLayer = foreground_instance_layer.resize(size, reducing_gap=100)

        (self.maskX, self.maskY), (self.maskX1, self.maskY1) = self.getMaskValues(self.mask)
        self.setRoundedCornerMask(
            self.foregroundLayer,
            self.maskX,
            self.maskY,
            self.maskX1,
            self.maskY1,
            self.mask,
            color=None,
            width=None,
            fill=255,
        )

        self.baseLayer.paste(
            self.foregroundLayer, (self.x, self.y), mask=self.foregroundLayer.split()[-1]
        )

        if self.color:
            self.addStrokeLayer(self.color)
            self.setRoundedCornerMask(
                self.strokeLayer,
                self.maskX,
                self.maskY,
                self.maskX1,
                self.maskY1,
                self.mask,
                color="white",
                width=self.stroke,
                fill=0,
            )
            self.baseLayer.paste(
                self.strokeLayer, (self.x, self.y), mask=self.strokeLayer.split()[-1]
            )

        if self.textLayerContext:
            self.setText(
                self.textLayerContext["index"],
                self.textLayerContext["text"] or "null",
                self.textLayerContext["size"],
                self.textLayerContext["family"],
                self.textLayerContext["color"],
                self.textLayerContext["x"],
                self.textLayerContext["y"],
                self.textLayerContext["stroke"],
                self.textLayerContext["strokeColor"],
                self.textLayerContext["spacing"],
                self.textLayerContext["align"],
            )

        for index, textLayer in self.textLayers.items():
            textImageLayer = textLayer["textImageLayer"]
            self.baseLayer.paste(textImageLayer, (0, 0), mask=textImageLayer.split()[-1])

        return self.baseLayer.toqpixmap()

    def addText(self, context):
        self.setText(
            context["index"],
            context["text"] or "null",
            context["size"],
            context["family"],
            context["color"],
            context["x"],
            context["y"],
            context["stroke"],
            context["strokeColor"],
            context["spacing"],
            context["align"],
        )

        for index, textLayer in self.textLayers.items():
            textImageLayer = textLayer["textImageLayer"]
            self.baseLayer.paste(textImageLayer, (0, 0), mask=textImageLayer.split()[-1])

        return self.baseLayer.toqpixmap()

    def addTextList(self, contextList):
        for contexts in contextList:
            context = dict()
            for each in contexts:
                context.update(each)
            self.addText(context)

        return self.baseLayer.toqpixmap()

    def setText(self, index, text, size, family, color, x, y, stroke, strokeColor, spacing, align):
        textImageLayer = Image.new("RGBA", self.backgroundLayer.size, (255, 255, 255, 0))

        draw = ImageDraw.Draw(textImageLayer)
        font = ImageFont.truetype(family, size)

        formattedText = text.replace("\\n", "\n")  # .replace("\\t", "\t")

        textbbox = draw.textbbox((0, 0), formattedText, font=font)

        self.textLayers[index] = {
            "textImageLayer": textImageLayer,
            "textbbox": textbbox,
            "text": formattedText,
            "x": x,
            "y": y,
        }

        # draw.text((6, 8), text, fill ="red", font = font,
        #           spacing = spacing, align ="left")

        draw.text(
            (x, y),
            formattedText,
            fill=color,
            font=font,
            # anchor=None, # "lt",
            spacing=spacing,
            align=align,  # "left", "center" or "right".
            direction=None,  # "ltr", # "ttb", #  "rtl" (right to left), "ltr" (left to right) or "ttb"  (top to bottom). Requires libraqm.
            # features=None,
            # language=None,
            stroke_width=stroke,
            stroke_fill=strokeColor,
            # embedded_color=False,
            # font_size=None
        )

        return self.baseLayer.toqpixmap()

    def getMaskValues(self, value):
        min_dimension = min(self.foregroundLayer.size)
        max_dimension = max(self.foregroundLayer.size)

        minLimit = min_dimension / 2
        maxLimit = max_dimension / 2

        if minLimit <= value and maxLimit >= value:
            radiusAdjusted = value - minLimit

            if self.foregroundLayer.width >= self.foregroundLayer.height:
                maskX, maskY = radiusAdjusted, 0
                maskX1, maskY1 = (
                    self.foregroundLayer.width - radiusAdjusted,
                    self.foregroundLayer.height,
                )

            if self.foregroundLayer.width <= self.foregroundLayer.height:
                maskX, maskY = 0, radiusAdjusted
                maskX1, maskY1 = (
                    self.foregroundLayer.width,
                    self.foregroundLayer.height - radiusAdjusted,
                )

        elif maxLimit <= value:
            if self.foregroundLayer.width > self.foregroundLayer.height:
                xRadius = value - minLimit
                yRadius = value - maxLimit

            elif self.foregroundLayer.width < self.foregroundLayer.height:
                xRadius = value - maxLimit
                yRadius = value - minLimit

            elif self.foregroundLayer.width == self.foregroundLayer.height:
                xRadius = value - maxLimit
                yRadius = value - maxLimit

            maskX, maskY = xRadius, yRadius
            maskX1, maskY1 = (
                self.foregroundLayer.width - xRadius,
                self.foregroundLayer.height - yRadius,
            )

        elif (self.foregroundLayer.width / 2) + (self.foregroundLayer.height / 2) <= value:
            maskX, maskY = self.foregroundLayer.width / 2, self.foregroundLayer.height / 2
            maskX1, maskY1 = self.foregroundLayer.width / 2, self.foregroundLayer.height / 2
        else:
            maskX, maskY = 0, 0
            maskX1, maskY1 = self.foregroundLayer.size

        return (maskX, maskY), (maskX1, maskY1)

    def setRoundedCornerMask(self, layer, x, y, x1, y1, radius, color=None, width=None, fill=255):
        # Create rounded corner mask
        mask = Image.new("L", layer.size, 0)
        # mask = Image.new("RGBA", layer.size, (255, 255, 255, 0))

        draw = ImageDraw.Draw(mask)

        try:
            draw.rounded_rectangle(
                [(x, y), (x1, y1)],
                radius=radius,
                fill=fill,
                outline=color,
                width=width,
                # corners=None
            )
            layer.putalpha(mask)
        except:
            pass


if __name__ == "__main__":
    pass
