# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, constants modulesource code.


TOOL_NAME = "MC_Cache_Tool"
TOOL_IOCN = "cache-tool"
TOOL_TITLE = "Motion-Craft Cache Tool"
RELEASE = "v1"
VERSION = "0.0.1-beta.2"
AUTHOR = "subing85@gmail.com"
DESCRIPTION = "Motion-Craft cache Tool Internal usage."
COPYRIGHT_LABEL = "Copyright (c) 2025, Motion-Craft Technology All rights reserved."

HELP_URL = "https://subing85.github.io/"

GUI_THEMES = ["light", "dark"]

FONT_SIZE = 12

PROJECT_PRESET_NAME = "cache-project.preset"

LOAD_FROM_DATA = False
CLEAR_CACHE = True

TIMEOUT = None

INPUT_EXTENTIONS = ["ma", "mb", "blend"]
# MAYA_FORMATS = ["mayaAscii", "mayaBinary"]
# MAYA_EXTENTIONS = ["ma", "mb"]

NODE_ICON_NAME = "node"

PROJECT_CONTEXT_LIST = [
    {
        "name": "project",
        "label": "Project Path",
        "key": "projectPath",
        "index": 0,
        "icon": "project",
        "application": False,
        "value": None,
    },
    {
        "name": "maya",
        "label": "Maya Directory",
        "key": "mayaDirectory",
        "index": 1,
        "icon": "maya",
        "application": True,
        "extensions": ["ma", "mb"],
        "formats": ["mayaAscii", "mayaBinary"],
        "value": "C:/Program Files/Autodesk/Maya2023",
        "paths": ["bin", "mayapy"],
        "importCode": "mayaImport",
        "exportCode": "mayaExport",
        "importAction": "scripts.maya.ImportSource",
        "exportAction": "scripts.maya.ExportCache",
        "defaultNodes": ["persp", "top", "front", "side"],
        "nodeNames": ["model", "models", "geometry", "camera"],
        "startupContext": dict(),
        "commands": "{applicationPath}<>{pythonCode}",
        "plugins": [
            "AbcExport",
            # "AbcImport",
            # "OpenEXRLoader",
            # "animImportExport",
            # "atomImportExport",
            # "mtoa",
            # "mtoh",
            # "gpuCache",
            # "xgenToolkit",
        ],
    },
    {
        "name": "blender",
        "label": "Blender Directory",
        "key": "blenderDirectory",
        "index": 2,
        "icon": "blender",
        "application": True,
        "extensions": ["blend"],
        "formats": ["blend"],
        "value": "C:/Program Files/Blender Foundation/Blender 4.0",
        "paths": ["blender"],
        "importCode": "blenderImport",
        "exportCode": "blenderExport",
        "importAction": "scripts.blender.ImportSource",
        "exportAction": "scripts.blender.ExportCache",
        "defaultNodes": ["persp", "top", "front", "side"],
        "nodeNames": ["model", "models", "geometry", "camera"],
        "startupContext": dict(),
        "sourceFile": True,
        "commands": "{applicationPath}<>--python-use-system-env<>--background<>{sourceFile}<>--python<>{pythonCode}",
        "plugins": [],
    },
]


# MAYA_ROOT_DIRECTORY = "C:/Program Files/Autodesk/Maya2023"  #

# =====================================================================================================================================================
# MAYA_PYTHON_LIB = [
#     ["bin", "python39.zip"],
#     ["Python", "DLLs"],
#     ["Python", "ib"],
#     ["bin"],
#     ["Python"],
# ]
# =====================================================================================================================================================

# =====================================================================================================================================================
# MAYA_PYTHON_LIB_PATHS = [
#     "C:/Program Files/Autodesk/Maya2023/bin/python39.zip",
#     "C:/Program Files/Autodesk/Maya2023/Python/DLLs",
#     "C:/Program Files/Autodesk/Maya2023/Python/lib",
#     "C:/Program Files/Autodesk/Maya2023/bin",
#     "C:/Users/batman/AppData/Roaming/Python/Python39/site-packages",
#     "C:/Program Files/Autodesk/Maya2023/Python",
#     "C:/Program Files/Autodesk/Maya2023/Python/lib/site-packages",
# ]
# =====================================================================================================================================================

# MAYA_PY_FOLDERS = ["bin", "mayapy.exe"]

# MAYA_DEFAULT_NODES = ["persp", "top", "front", "side"]


# =====================================================================================================================================================
# MAYA_PLUGINS = [
#     "AbcExport",
#     "AbcImport",
#     "OpenEXRLoader",
#     "animImportExport",
#     "atomImportExport",
#     "mtoa",
#     "mtoh",
#     "gpuCache",
#     "xgenToolkit",
# ]
# =====================================================================================================================================================

UNIT_LIST = {
    "value": "centimeter",
    "values": [
        "millimeter",
        "centimeter",
        "meter",
        "inch",
        "foot",
        "yard",
    ],
}

AXIS_LIST = {"value": "y", "values": ["x", "y"]}

FPS_LIST = {
    "value": {"label": "pal", "index": 25},
    "values": [
        {"label": "film", "index": 24},
        {"label": "pal", "index": 25},
        {"label": "ntsc", "index": 30},
    ],
}

CACHE_TYPES = {
    "value": "Alembic",
    "values": [
        "Alembic",
        "USD",
        "FBX",
        "Alembic + USD",
        "USD + FBX",
        "Alembic + FBX",
        "Alembic + USD + FBX",
    ],
}

KINDS = [
    "episode-0001",
    "episode-0002",
    "episode-0003",
    "episode-0004",
    "episode-0005",
    "episode-0006",
    "episode-0007",
    "episode-0008",
    "episode-0009",
    "episode-0010",
    "episode-0011",
    "episode-0012",
    "episode-0013",
    "episode-0014",
    "episode-0015",
    "episode-0016",
    "episode-0017",
    "episode-0018",
    "episode-0019",
    "episode-0020",
    "episode-0021",
    "episode-0022",
]

SEQUENCES = [
    "sequence-0001",
    "sequence-0002",
    "sequence-0003",
    "sequence-0004",
    "sequence-0005",
    "sequence-0006",
    "sequence-0007",
    "sequence-0008",
    "sequence-0009",
    "sequence-0010",
    "sequence-0011",
    "sequence-0012",
    "sequence-0013",
    "sequence-0014",
    "sequence-0015",
    "sequence-0016",
    "sequence-0017",
    "sequence-0018",
    "sequence-0019",
    "sequence-0020",
    "sequence-0021",
    "sequence-0021",
    "sequence-0021",
    "sequence-0022",
    "sequence-0023",
    "sequence-0024",
    "sequence-0025",
    "sequence-0026",
    "sequence-0027",
    "sequence-0028",
    "sequence-0029",
    "sequence-0030",
    "sequence-0031",
    "sequence-0032",
    "sequence-0033",
    "sequence-0034",
    "sequence-0035",
    "sequence-0036",
    "sequence-0037",
    "sequence-0038",
    "sequence-0039",
    "sequence-0040",
    "sequence-0041",
    "sequence-0042",
    "sequence-0043",
    "sequence-0044",
    "sequence-0045",
    "sequence-0046",
    "sequence-0047",
    "sequence-0048",
    "sequence-0049",
    "sequence-0050",
]

SHOTS = [
    "shot-0001",
    "shot-0002",
    "shot-0003",
    "shot-0004",
    "shot-0005",
    "shot-0006",
    "shot-0007",
    "shot-0008",
    "shot-0009",
    "shot-0010",
    "shot-0011",
    "shot-0012",
    "shot-0013",
    "shot-0014",
    "shot-0015",
    "shot-0016",
    "shot-0017",
    "shot-0018",
    "shot-0019",
    "shot-0020",
    "shot-0021",
    "shot-0022",
    "shot-0023",
    "shot-0024",
    "shot-0025",
    "shot-0026",
    "shot-0027",
    "shot-0028",
    "shot-0029",
    "shot-0030",
    "shot-0031",
    "shot-0032",
    "shot-0033",
    "shot-0034",
    "shot-0035",
    "shot-0036",
    "shot-0037",
    "shot-0038",
    "shot-0039",
    "shot-0040",
    "shot-0041",
    "shot-0042",
    "shot-0043",
    "shot-0044",
    "shot-0045",
    "shot-0046",
    "shot-0047",
    "shot-0048",
    "shot-0049",
    "shot-0050",
    "shot-0051",
    "shot-0052",
    "shot-0053",
    "shot-0054",
    "shot-0055",
    "shot-0056",
    "shot-0057",
    "shot-0058",
    "shot-0059",
    "shot-0060",
    "shot-0061",
    "shot-0062",
    "shot-0063",
    "shot-0064",
    "shot-0065",
    "shot-0066",
    "shot-0067",
    "shot-0068",
    "shot-0069",
    "shot-0070",
    "shot-0071",
    "shot-0072",
    "shot-0073",
    "shot-0074",
    "shot-0075",
    "shot-0076",
    "shot-0077",
    "shot-0078",
    "shot-0079",
    "shot-0080",
    "shot-0081",
    "shot-0082",
    "shot-0083",
    "shot-0084",
    "shot-0085",
    "shot-0086",
    "shot-0087",
    "shot-0088",
    "shot-0089",
    "shot-0090",
    "shot-0091",
    "shot-0092",
    "shot-0093",
    "shot-0094",
    "shot-0095",
    "shot-0096",
    "shot-0097",
    "shot-0098",
    "shot-0099",
    "shot-0100",
]

TASKS = ["animation"]

DEFAULT_FRAME_START = 1000
DEFAULT_FRAME_END = 1001

DEFAULT_VERSION = "00001"

VERSION_PADDING = 5
