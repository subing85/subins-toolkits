# Copyright (c) 2025, Motion-Craft-Works Production All rights reserved.
# Author: Subin. Gopi (motioncraftworks85@gmail.com, subing85@gmail.com).
# Description: Motion-Craft-Works Evi(ID - Card)  utils module.
# WARNING! All changes made in this file will be lost when recompiling UI file!

import os
import csv
import stat
import glob
import shutil

from xml.dom import minidom
import xml.etree.ElementTree as ElementTree

from kore import logger
from kore import constants

LOGGER = logger.getLogger(__name__)


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


def dirname(filepath):
    return os.path.dirname(filepath)


def hasFileExists(filepath):
    """ """

    if not filepath:
        return None

    absfilepath = os.path.expandvars(filepath)
    return os.path.isfile(absfilepath)


def hasPathExists(path):
    """ """

    if not path:
        return False

    abspath = os.path.expandvars(path)
    return os.path.isdir(abspath)


def makedirs(path):
    """ """

    if os.path.isdir(path):
        return

    os.makedirs(path)


def basename(filepath):
    return os.path.basename(filepath)


def fileExtenstion(filepath):
    return os.path.splitext(filepath)[-1]


def fileNameSplit(filepath):
    filename, extension = os.path.splitext(os.path.basename(filepath))
    return filename, extension


def copyFile(source, destination):
    if hasFileExists(destination):
        try:
            os.chmod(destination, stat.S_IWRITE)
            os.remove(destination)
            valid = True
        except Exception as error:
            valid = False
            LOGGER.error(error)

    if not hasPathExists(dirname(destination)):
        os.makedirs(dirname(destination))

    try:
        shutil.copy2(source, destination)
        valid = True
    except Exception as error:
        LOGGER.error(error)
        valid = False

    return valid


def collectFilesContextList(directory, extenstion, reverse=False):
    pathname = "%s/*.%s" % (pathResolver(directory), extenstion)

    files = sorted(glob.glob(pathname), reverse=reverse)

    contextList = [
        {
            "filepath": None,
            "filename": "Null",
            "extension": None,
        }
    ]

    for each in files:
        filename, extension = fileNameSplit(each)
        context = {
            "filepath": pathResolver(each),
            "filename": filename,
            "extension": extension,
        }

        contextList.append(context)

    return contextList


def pixelsToInches(pixelsWidth, pixelsHeight, dpi=300):
    # Convert pixels to inches
    width_in_inches = pixelsWidth / dpi
    height_in_inches = pixelsHeight / dpi

    return width_in_inches, height_in_inches


def inchesToPixels(inchwidth, inchHeight, dpi=300):
    width_in_pixels = inchwidth * dpi
    height_in_pixels = inchwidth * dpi
    return width_in_pixels, height_in_pixels


def pixelsTocentimeters(pixelsWidth, pixelsHeight, dpi=300):
    width_in_inches, height_in_inches = pixelsToInches(pixelsWidth, pixelsHeight, dpi=dpi)

    width_in_cm = width_in_inches * 2.54
    height_in_cm = height_in_inches * 2.54

    return width_in_cm, height_in_cm


def exportTemplate(filepath, inputContext, barcodeContext, fieldContextList):
    elementRoot = ElementTree.Element(
        constants.NAME,
        release=constants.RELEASE,
        version=constants.VERSION,
        author=constants.AUTHOR,
        description=constants.DESCRIPTION,
        mcw=constants.MCW,
    )

    templateElement = ElementTree.SubElement(elementRoot, "eve", type="template")

    inputElement = ElementTree.SubElement(templateElement, "collection", name="input", type="dict")
    barcodeElement = ElementTree.SubElement(
        templateElement, "collection", name="barcode", type="dict"
    )
    fieldElement = ElementTree.SubElement(templateElement, "collection", name="field", type="list")

    for name, value in inputContext.items():
        parameterElement = ElementTree.SubElement(
            inputElement,
            "parameter",
            name=name,
            default=str(value["default"]),
            type=type(value["default"]).__name__,
        )

    for name, value in barcodeContext.items():
        parameterElement = ElementTree.SubElement(
            barcodeElement,
            "parameter",
            name=name,
            default=str(value["default"]),
            type=type(value["default"]).__name__,
        )

    for fieldContexts in fieldContextList:
        filedParameterGroupElement = ElementTree.SubElement(
            fieldElement,
            "parameterGroup",
            name="fieldProperties",
            index=str(fieldContexts[0]["index"]["default"]),
            type=type(fieldContextList).__name__,
        )

        for fieldContext in fieldContexts:
            for name, value in fieldContext.items():
                parameterElement = ElementTree.SubElement(
                    filedParameterGroupElement,
                    "parameter",
                    name=name,
                    default=str(value["default"]),
                    type=type(value["default"]).__name__,
                )

    roughString = ElementTree.tostring(elementRoot)
    reparsed = minidom.parseString(roughString)
    prettyXml = reparsed.toprettyxml()

    element = ElementTree.XML(prettyXml)
    tree = ElementTree.ElementTree(element)
    tree.write(filepath)

    return True, "Succeed!..."


def dataTypeResolver(typed, value):
    if typed == "int":
        result = int(value)
    elif typed == "float":
        result = float(value)
    elif typed == "bool":
        result = value == "True"
    else:
        result = value

    return result


def importTemplate(filepath):
    elementTree = ElementTree.parse(filepath)
    elementRoot = elementTree.getroot()
    templateElements = elementRoot[0]

    inputContext, barcodeContext, fieldContextList = dict(), dict(), list()

    if templateElements.get("type") != "template":
        LOGGER.warning("Invalid template file, %s" % filepath)

    for x in templateElements:
        if x.get("name") == "input":
            inputElements = x
            break
    else:
        inputElements = None

    for x in templateElements:
        if x.get("name") == "barcode":
            barcodeElements = x
            break
    else:
        barcodeElements = None

    for x in templateElements:
        if x.get("name") == "field":
            fieldElements = x
            break
    else:
        fieldElements = None

    if inputElements:
        for inputElement in inputElements:
            value = dataTypeResolver(inputElement.get("type"), inputElement.get("default"))
            inputContext[inputElement.get("name")] = {"default": value}

    if barcodeElements:
        for barcodeElement in barcodeElements:
            value = dataTypeResolver(barcodeElement.get("type"), barcodeElement.get("default"))
            barcodeContext[barcodeElement.get("name")] = {"default": value}

    if fieldElements:
        for fieldElement in fieldElements:
            fieldContexts = dict()
            for fieldProperty in fieldElement:
                value = dataTypeResolver(fieldProperty.get("type"), fieldProperty.get("default"))
                fieldContexts[fieldProperty.get("name")] = {"default": value}
            fieldContextList.append(fieldContexts)

    return inputContext, barcodeContext, fieldContextList


def prettyXml(element):
    roughString = ElementTree.tostring(element)

    reparsed = minidom.parseString(roughString)
    prettyXml = reparsed.toprettyxml()


def importCSV(filepath):
    with open(filepath, mode="r") as file:
        try:
            csv_content = csv.reader(file)
            result = [each for each in csv_content]
        except Exception as error:
            result = None

    contextList = list()

    if not result:
        return contextList

    for child in result[1:]:
        contextList.append(dict(zip(result[0], child)))

    return contextList


def imageFile(filepath):
    for x in constants.IMAGE_EXTENSTIONS:
        fullFilepath = "%s.%s" % (filepath, x)

        if hasFileExists(fullFilepath):
            filename = basename(fullFilepath)
            break
    else:
        fullFilepath, filename = None, None

    return fullFilepath, filename


def saveFile(inputs, filepath):
    elementRoot = ElementTree.Element(
        constants.NAME,
        release=constants.RELEASE,
        version=constants.VERSION,
        author=constants.AUTHOR,
        description=constants.DESCRIPTION,
        mcw=constants.MCW,
    )

    sceneElement = ElementTree.SubElement(elementRoot, "eve", type="scene")

    templateElement = ElementTree.SubElement(
        sceneElement, "collection", name="template", type="dict"
    )

    templateContext = inputs[0]
    pathContext = inputs[1]
    outlineContextList = inputs[2]

    for k, v in templateContext.items():
        parameterElement = ElementTree.SubElement(
            templateElement,
            "parameter",
            name=k,
            default=str(v),
            type=type(v).__name__,
        )

    pathElement = ElementTree.SubElement(sceneElement, "eve", type="path")

    for k, v in pathContext.items():
        parameterElement = ElementTree.SubElement(
            pathElement,
            "parameter",
            name=k,
            default=str(v),
            type=type(v).__name__,
        )

    for outlineContext in outlineContextList:
        outlineElement = ElementTree.SubElement(
            sceneElement,
            "collection",
            name="outline",
            index=str(outlineContext["index"]),
            type="int",
        )

        inputElement = ElementTree.SubElement(
            outlineElement, "collection", name="inputContext", type="dict"
        )

        for name, context in outlineContext["inputContext"].items():
            if context.get("value") is not None:
                parameterElement = ElementTree.SubElement(
                    inputElement,
                    "parameter",
                    name=name,
                    default=str(context["default"]),
                    value=str(context["value"]),
                    type=type(context["default"]).__name__,
                )
            else:
                parameterElement = ElementTree.SubElement(
                    inputElement,
                    "parameter",
                    name=name,
                    default=str(context["default"]),
                    type=type(context["default"]).__name__,
                )

        fieldElement = ElementTree.SubElement(
            outlineElement, "collection", name="fieldContextList", type="list"
        )

        for fieldContexts in outlineContext["fieldContextList"]:
            filedParameterGroupElement = ElementTree.SubElement(
                fieldElement,
                "parameterGroup",
                name="fieldProperties",
                index=str(fieldContexts["index"]["default"]),
                type="int",
            )

            for name, context in fieldContexts.items():
                if context.get("value") is not None:
                    parameterElement = ElementTree.SubElement(
                        filedParameterGroupElement,
                        "parameter",
                        name=name,
                        default=str(context["default"]),
                        value=str(context["value"]),
                        type=type(context["default"]).__name__,
                    )
                else:
                    parameterElement = ElementTree.SubElement(
                        filedParameterGroupElement,
                        "parameter",
                        name=name,
                        default=str(context["default"]),
                        type=type(context["default"]).__name__,
                    )

    roughString = ElementTree.tostring(elementRoot)
    reparsed = minidom.parseString(roughString)
    prettyXml = reparsed.toprettyxml()

    element = ElementTree.XML(prettyXml)
    tree = ElementTree.ElementTree(element)
    tree.write(filepath)

    return True, "Succeed!..."


def openFile(filepath):
    elementTree = ElementTree.parse(filepath)
    elementRoot = elementTree.getroot()
    sceneElement = elementRoot[0]

    templateElements = sceneElement[0]
    pathElements = sceneElement[1]
    outlineElements = sceneElement[2:]

    templateContext = dict()
    pathContext = dict()
    outlineContextList = list()

    for x in templateElements:
        templateContext[x.get("name")] = x.get("default")

    for x in pathElements:
        pathContext[x.get("name")] = x.get("default")

    outlinesContextList = list()

    for outlines in outlineElements:
        # print("\n", outlines.attrib)
        value = dataTypeResolver(outlines.get("type"), outlines.get("index"))
        outlineContext = {"index": value}

        for outline in outlines:
            if outline.get("type") == "dict":
                currentContext = dict()
                for x in outline:
                    defaultValue = dataTypeResolver(x.get("type"), x.get("default"))
                    currentContext[x.get("name")] = {"default": defaultValue}
                    if x.get("value"):
                        overrideValue = dataTypeResolver(x.get("type"), x.get("value"))
                        currentContext[x.get("name")].update({"value": overrideValue})

            elif outline.get("type") == "list":
                currentContext = list()

                for each in outline:
                    eachContext = dict()
                    for x in each:
                        # attributeContext = x.attrib.copy()
                        # attributeContext.pop("name")
                        # eachContext[x.get("name")] = attributeContext

                        defaultValue = dataTypeResolver(x.get("type"), x.get("default"))
                        eachContext[x.get("name")] = {"default": defaultValue}
                        if x.get("value"):
                            overrideValue = dataTypeResolver(x.get("type"), x.get("value"))
                            eachContext[x.get("name")].update({"value": overrideValue})

                    currentContext.append(eachContext)
            else:
                currentContext = str()
            outlineContext[outline.get("name")] = currentContext

        outlinesContextList.append(outlineContext)

    # import json
    # with open("C:/Users/batman/Documents/evi-resolve/project_01/tmp-01.json", "w") as target:
    #     target.write(json.dumps(outlinesContextList, indent=4))

    # for x in outlinesContextList:
    #     print(x["fieldContextList"][0]["underline"]['default'])
    #     print(type(x["fieldContextList"][0]["underline"]['default']))

    # from pprint import pprint
    # pprint(templateContext)

    return templateContext, pathContext, outlinesContextList


def aspectScale(width, height, scale):
    increment = scale - 100
    aspectRatio = width / height

    if width > height:
        new_width = width + increment
        new_height = (width + increment) / aspectRatio
    elif width < height:
        new_width = aspectRatio * (height + increment)
        new_height = height + increment
    else:
        new_width = width + increment
        new_height = height + increment

    return new_width, new_height


if __name__ == "__main__":
    filepath = "C:/Users/batman/Documents/evi-resolve/templates/test-0001.xml"
    fieldContextList = importTemplate(filepath)

    from pprint import pprint

    pprint(fieldContextList[1])
