# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, maya batch source code.


from __future__ import absolute_import

from kore import utils
from kore import constant


class ImportFile(object):
    name = "importCode"
    prefix = "import"

    @classmethod
    def doIt(cls, filepath, *args, **kwargs):
        logger = kwargs.get("logger", False)
        applicationDirectory = kwargs.get("value")
        progressCallback = kwargs.get("progressCallback")

        progressCallback.emit("%s file, %s" % (kwargs["name"], filepath))
        progressCallback.emit("Writing python script to read %s file" % kwargs["name"])

        scriptFilePath, jsonFilePath = ImportFile.script(filepath, **kwargs)

        applicationPath = utils.pathResolver(applicationDirectory, folders=kwargs["paths"])

        # commands = [
        #     utils.pathResolver(applicationPath, folders=kwargs["paths"]),
        #     scriptFilePath,
        # ]

        flags = {"applicationPath": applicationPath, "pythonCode": scriptFilePath}

        if kwargs.get("sourceFile"):
            flags["sourceFile"] = filepath

        commands = kwargs["commands"].format(**flags).split("<>")

        # C:/Program Files/Autodesk/Maya2023/bin/mayapy C:/Users/batman/Documents/orbit/temp/orbit-import-2333812216.py
        # C:/Program Files/Blender Foundation/Blender 4.0/bin/blender --python-use-system-env --background --python C:/Users/batman/Documents/orbit/temp/orbit-import-87880579.py

        progressCallback.emit("Command, %s" % " ".join(commands))
        progressCallback.emit("Started, subprocess")

        valid, process = utils.executeSubprocess(
            commands, False, None, constant.TIMEOUT, logger=logger  # shell  # env  # timeout
        )
        progressCallback.emit("Completed, subprocess")

        result = ImportFile.result(jsonFilePath)

        context = {
            "valid": valid,
            "process": process,
            "result": result,
        }

        if constant.CLEAR_CACHE:
            ImportFile.clear([scriptFilePath, jsonFilePath])

        return context

    @classmethod
    def script(cls, filepath, **kwargs):
        scriptTemaplate = utils.getCodeTemaplate(
            kwargs["importCode"], fromData=constant.LOAD_FROM_DATA
        )

        tempName = utils.getTempName(ImportFile.prefix)
        jsonFilePath = utils.getTempJsonPath(tempName)

        context = {
            "importAction": kwargs.get("importAction"),
            "filepath": filepath,
            "defaultNodes": kwargs.get("defaultNodes"),
            "nodeNames": kwargs.get("nodeNames"),
            "jsonFilepath": jsonFilePath,
        }

        pythonCode = scriptTemaplate.render(context=context)

        scriptFilePath = utils.getTempScriptPath(tempName)

        utils.writeData(scriptFilePath, pythonCode)

        return scriptFilePath, jsonFilePath

    @classmethod
    def result(cls, filepath):
        return utils.readJsonFile(filepath)

    @classmethod
    def clear(cls, filePaths):
        for filePath in filePaths:
            utils.deleteFiles(filePath)


class ExportCache(object):
    name = "exportCode"
    prefix = "export"

    @classmethod
    def doIt(cls, filepath, *args, **kwargs):
        logger = kwargs.get("logger", False)
        applicationDirectory = kwargs.get("value")
        progressCallback = kwargs.get("progressCallback")

        progressCallback.emit("%s file, %s" % (kwargs["name"], filepath))
        progressCallback.emit("Writing python script to read %s file" % kwargs["name"])

        scriptFilePath, jsonFilePath = ExportCache.script(filepath, **kwargs)

        applicationPath = utils.pathResolver(applicationDirectory, folders=kwargs["paths"])

        # commands = [
        #     utils.pathResolver(applicationDirectory, folders=kwargs["paths"]),
        #     scriptFilePath,
        # ]

        flags = {"applicationPath": applicationPath, "pythonCode": scriptFilePath}
        if kwargs.get("sourceFile"):
            flags["sourceFile"] = filepath

        commands = kwargs["commands"].format(**flags).split("<>")

        progressCallback.emit("Command, %s" % " ".join(commands))
        progressCallback.emit("Started, subprocess")

        valid, process = utils.executeSubprocess(
            commands, False, None, constant.TIMEOUT, logger=logger  # shell  # env  # timeout
        )

        progressCallback.emit("Completed, subprocess")

        result = ExportCache.result(jsonFilePath)

        context = {
            "valid": valid,
            "process": process,
            "result": result,
        }

        if constant.CLEAR_CACHE:
            ExportCache.clear([scriptFilePath, jsonFilePath])

        return context

    @classmethod
    def script(cls, filepath, **kwargs):
        scriptTemaplate = utils.getCodeTemaplate(
            kwargs["exportCode"], fromData=constant.LOAD_FROM_DATA
        )

        tempName = utils.getTempName(ExportCache.prefix)
        jsonFilePath = utils.getTempJsonPath(tempName)

        context = {
            "exportAction": kwargs.get("exportAction"),
            "filepath": filepath,
            "frameStart": kwargs.get("frameStart"),
            "frameEnd": kwargs.get("frameEnd"),
            "nodes": kwargs.get("nodes"),
            "localPath": kwargs.get("localPath"),
            "cameraFBX": kwargs.get("cameraFBX"),
            "cache": kwargs.get("cache"),
            "jsonFilepath": jsonFilePath,
        }

        pythonCode = scriptTemaplate.render(context=context)
        scriptFilePath = utils.getTempScriptPath(tempName)

        utils.writeData(scriptFilePath, pythonCode)

        return scriptFilePath, jsonFilePath

    @classmethod
    def result(cls, filepath):
        return utils.readJsonFile(filepath)

    @classmethod
    def clear(cls, filePaths):
        for filePath in filePaths:
            utils.deleteFiles(filePath)


if __name__ == "__main__":
    pass
