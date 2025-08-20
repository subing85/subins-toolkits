# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, utils source code.


from __future__ import absolute_import

import os
import re
import json
import stat
import uuid
import random
import getpass
import tempfile
import subprocess
import webbrowser

import resources

from datetime import datetime

from jinja2 import Template
from jinja2 import Environment
from jinja2 import FileSystemLoader

from kore import logger
from kore import constant

LOGGER = logger.getLogger(__name__)

CURRENT_PATH = os.path.dirname(__file__)


def getProjectContextList():
    return constant.PROJECT_CONTEXT_LIST


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


def fileExtenstion(filepath):
    return os.path.splitext(filepath)[-1].rsplit(".", 1)[-1]


def fileName(filepath, extenstion=True):
    if extenstion:
        name = os.path.basename(filepath)
        return name

    name = os.path.splitext(os.path.basename(filepath))[0]
    return name


def folderName(path):
    return fileName(path, extenstion=False)


def dirname(path):
    return os.path.dirname(path)


def isPath(path):
    return os.path.isabs(path)


def hasFileExists(filepath):
    if not filepath:
        return None

    absfilepath = os.path.expandvars(filepath)
    return os.path.isfile(absfilepath)


def hasPathExists(path):
    if not path:
        return False

    abspath = os.path.expandvars(path)
    if os.path.isdir(abspath):
        return True

    if hasFile(abspath):
        abspath = os.path.dirname(abspath)
        return os.path.isdir(abspath)

    return False


def hasFile(filepath):
    dirname, extenstion = os.path.splitext(filepath)
    return True if extenstion else False


def makedirs(path):
    if not path:
        return

    abspath = os.path.expandvars(path)
    if hasFile(abspath):
        abspath = os.path.dirname(abspath)

    if os.path.isdir(abspath):
        return

    os.makedirs(abspath)
    LOGGER.info("Created new directory, %s" % abspath)


def deleteFiles(filepaths, verbose=False):
    if isinstance(filepaths, str):
        filepaths = [filepaths]

    validList = list()

    for filepath in filepaths:
        filepath = pathResolver(filepath)
        if not os.path.isfile(filepath):
            return
        try:
            os.chmod(filepath, stat.S_IWRITE)
            valid = True
        except Exception as error:
            valid = False
        try:
            os.remove(filepath)
            valid = True
        except Exception as error:
            valid = False

        if valid and verbose:
            LOGGER.warning("Removed exists file, %s" % filepath)

        validList.append(valid)

    return False if False in validList else True


def openUrl(path):
    webbrowser.open(path)


def getDateTimes(context=None):
    if isinstance(context, str):
        return context

    now = context if context else datetime.now()
    date_time = now.strftime("%Y-%m-%d %I:%M:%S:%p")
    return date_time


def getUserName():
    return getpass.getuser()


def writeJsonFile(context, filepath):
    makedirs(filepath)

    with open(filepath, "w") as target:
        target.write(json.dumps(context, indent=4))


def readJsonFile(filepath):  # remove this function
    if not hasFileExists(filepath):
        return dict()

    with open(filepath, "r") as target:
        return json.load(target)


def writeData(filepath, content):
    makedirs(filepath)
    with open(filepath, "w") as data:
        data.write(content)
        return filepath


def getTmpDirectory():
    return tempfile.gettempdir()


def getTempName(prefix):
    name = "orbit-%s-%s" % (prefix, int(uuid.uuid1().time_low))
    # name = "orbit-%s-%s" % (prefix, int(uuid.uuid1().time))

    return name


def getTempScriptPath(name):
    scriptPath = pathResolver(
        resources.getOrbitPath(),
        folders=["temp"],
        filename="%s.py" % name,
    )
    makedirs(scriptPath)
    return scriptPath


def getTempJsonPath(name):
    jsonPath = pathResolver(
        resources.getOrbitPath(),
        folders=["temp"],
        filename="%s.json" % name,
    )
    makedirs(jsonPath)
    return jsonPath


def _executeSubprocess(commands, shell, env, communicate, wait):
    commands = [commands] if isinstance(commands, str) else commands

    process = subprocess.Popen(
        commands, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
    )

    _communicate = None
    if communicate:
        if wait:
            process.wait()
        _communicate = process.communicate()

    valid = True if process.returncode == 0 else False

    return valid, process, _communicate


def executeSubprocess(commands, shell, env, timeout, logger=False):
    parameters = {"shell": shell, "env": env}

    if not logger:
        parameters.update({"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL})

    try:
        subprocess.check_call(commands, **parameters)
        valid = True
    except subprocess.TimeoutExpired:
        LOGGER.warning("Command timed out.")
        valid = False
    except subprocess.CalledProcessError as error:
        LOGGER.error("Command failed with error: %s" % (str(error)))
        valid = False

    return valid, None


def getCodeTemaplate(code, fromData=False):
    if fromData:
        templateData = resources.getCodeData(code)
        template = Template(templateData)
    else:
        directory = resources.getCodePath()
        fileLoader = FileSystemLoader(directory)
        env = Environment(loader=fileLoader)
        template = env.get_template("%s.code" % code)

    return template


def decodeCommunicate(communicates, verbose=False):
    resultList = list()

    for communicate in communicates:
        text = communicate.decode()

        if verbose:
            print(text)

        # Use a regular expression to find the list inside the string
        match = re.search(
            r"{}\s*(.*?)\s*{}".format(constant.BATCH_START_COMMENTS, constant.BATCH_END_COMMENTS),
            text,
        )

        if match:
            result = match.group(1)  # group(1) to get content between the two markers
            resultList.append(eval(result))

    return resultList


def searchversions(directory, reverse=False):
    if not hasPathExists(directory):
        return list()

    folders = os.listdir(directory)

    pattern = re.compile(r"^\d{%s}$" % constant.VERSION_PADDING)
    filteredList = [item for item in folders if pattern.match(item)]

    versions = sorted(filteredList, reverse=True)

    return versions


def nextVersion(directory):
    versions = searchversions(directory, reverse=True)
    if not versions:
        return "1".zfill(constant.VERSION_PADDING)

    nextVersion = (str(int(versions[0]) + 1)).zfill(constant.VERSION_PADDING)
    return nextVersion


def randomNumber(range):
    return random.randrange(range)


if __name__ == "__main__":
    pass
