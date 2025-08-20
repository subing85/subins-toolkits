# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works ID - Card  Resolver resources source code.
# WARNING! All changes made in this file will be lost when recompiling UI file!

from __future__ import absolute_import

import os
import glob
import json
import pkgutil
import platform

from kore import logger

LOGGER = logger.getLogger(__name__)
CURRENT_PATH = os.path.dirname(__file__)


def getProjectPath():
    projectPath = os.path.abspath(
        os.path.join(os.environ["USERPROFILE"], "Documents", "evi-resolve")
    )
    return projectPath.replace("\\", "/")


def getTemplatePath():
    templatePath = os.path.abspath(os.path.join(getProjectPath(), "templates"))
    return templatePath.replace("\\", "/")


def pathResolver(path, folders=None, filename=None):
    folders = folders or []
    folders = [x for x in folders if x and isinstance(x, str)]
    expand_path = os.path.expandvars(path)

    if folders:
        expand_path = os.path.join(expand_path, *folders)
    if filename:
        expand_path = os.path.join(expand_path, filename)

    resolved_path = os.path.abspath(expand_path).replace("\\", "/")

    return resolved_path


def getIconPath():
    """Get the icon path from the resources.

    Args:
        None

    Returns:
        iconpath (str)

    Examples:
        iconPath = resources.getIconPath()
    """

    return os.path.join(CURRENT_PATH, "icons")


def getIconFilepath(name):
    """Get Specific Image.

    Args:
        name (str) : name of the image

    Returns:
        file path (str),when name exist.Otherwise,return unknown image path.

    Examples:
        specificimage = resources.getSpecificImage("maya2022")
    """

    if not name:
        filepath = getUnknownImage()
        return filepath

    iconPath = getIconPath()

    if not os.path.isdir(iconPath):
        iconPath = getIconPath()

    filepath = os.path.abspath(os.path.join(iconPath, "%s.png" % name))
    if os.path.isfile(filepath):
        return filepath.replace("\\", "/")

    filepath = getUnknownImage()
    return filepath


def getUnknownImage():
    """Get unknown Image.

    Args:
        None

    Returns:
        Unknownimage path (str)

    Examples:
        unknownimage = resources.getUnknownImage()
    """

    filepath = os.path.abspath(os.path.join(getIconPath(), "unknown.png"))
    return filepath.replace("\\", "/")


def getFontContext():
    context = {
        "name": {"field": "name", "value": "Enter field name here", "values": None},
        "value": {"field": "value", "value": "", "aaa": "Enter field value here", "values": None},
        "x": {"field": "x", "value": 100, "values": None},
        "y": {"field": "y", "value": 100, "values": None},
        "size": {"field": "size", "value": 16, "values": None},
        "family": {
            "field": "family",
            "value": "Myriad Pro Light",
            "aaa": "Times New Roman",
            "values": None,
        },
        "typed": {"field": "typed", "value": 0, "values": ["Normal", "Bold", "Italic"]},
        "color": {"field": "color", "value": (0, 0, 0), "values": None},
        "stroke": {"field": "stroke", "value": 0, "values": None},
        "strokeColor": {"field": "strokeColor", "value": (255, 255, 255), "values": None},
        "space": {"field": "space", "value": 0, "values": None},
    }

    return context


def getThumbnailPresets():
    context = {
        "resolution": 300,
        "size": [
            {"name": "Unknown", "width": 0, "height": 0},
            {"name": "CR79 ID Cards", "width": 2.050, "height": 3.303},
            {"name": "Extra Long 'Xtended' Cards", "width": 2.125, "height": 4.3},
            {"name": "CR100 ID Cards", "width": 2.63, "height": 3.88},
            {"name": "CR80 (Standard ID Card Size)", "width": 2.125, "height": 3.375},
        ],
        "shape": 0,
        "border": 0,
    }
    return context


if __name__ == "__main__":
    pass
