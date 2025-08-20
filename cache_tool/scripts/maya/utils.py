# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, scripts utils source code.


from __future__ import absolute_import

import os


def loadPlugins():
    """Load specified plugins into maya.

    This function enables the plugins defined in the `plugins` list.
    Any errors during loading will be logged as warnings.

    """

    from maya import cmds
    from maya import OpenMaya

    # List of addon names to load
    mayaPlugins = ["AbcExport", "fbxmaya", "mayaUsdPlugin"]

    for plugin in mayaPlugins:
        try:
            # Attempt to enable the plugin
            cmds.loadPlugin(plugin)
            OpenMaya.MGlobal.displayInfo("Success, plug-in loaded %s" % plugin)
        except Exception as error:
            # Log any errors during loading
            OpenMaya.MGlobal.displayWarning(str(error))


def setStartup(*args, **kwargs):
    """Set the startup configuration for Maya.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments containing configuration settings.
            Possible keys:
            - axis: Axis for transformation.
            - unit: Unit of measurement.
            - angle: Angle for rotation.
            - time: Time settings.

    Returns:
        bool: True if settings are successfully applied.
    """

    axis = kwargs.get("axis")
    unit = kwargs.get("unit")
    angle = kwargs.get("angle")
    time = kwargs.get("time")

    from maya import cmds

    cmds.upAxis(axis=axis)
    cmds.currentUnit(linear=unit, angle=angle, time=time)

    # Indicate successful execution
    return True


def openScene(filepath, **kwargs):
    """Open a Maya scene file.

    Args:
        filepath (str): The path to the .maya file to open.
        **kwargs: Additional parameters to modify the opening behavior.

    Returns:
        bool: True if the scene is opened successfully, None otherwise.
    """

    from maya import cmds

    # Parameters for opening the scene file
    parameter = {"open": True, "force": True, "ignoreVersion": True}
    # Update parameters with any additional kwargs
    parameter.update(kwargs)

    # Open the scene and check if successful

    cmds.file(filepath, **parameter)

    # Return True if the scene opened successfully
    return True


def getNodes(**kwargs):
    """Retrieve nodes from the current Maya scene.

    Args:
        **kwargs: Arbitrary keyword arguments.
            Possible keys:
            - nodeNames: List of node names to search for.
            - defaultNodes: Default nodes to consider.

    Returns:
        list: List of node names found in the scene.
    """

    nodeNames = kwargs.get("nodeNames")
    defaultNodes = kwargs.get("defaultNodes")

    from maya import cmds

    topLevelNodes = cmds.ls(assemblies=True, long=True)

    nodes = list()
    for node in topLevelNodes:
        if cmds.nodeType(node) != "transform":
            continue
        if node in defaultNodes:
            continue

        if not cmds.getAttr("%s.visibility" % node):
            continue

        for cacheName in nodeNames:
            if cacheName.lower() in node.lower():
                if node in nodes:
                    continue
                nodes.append(node)
                break

        children = cmds.listRelatives(node, children=True, fullPath=True, type="transform")

        if not children:
            continue

        for child in children:
            for cacheName in nodeNames:
                if cacheName.lower() in child.lower():
                    break
            else:
                child = None

        if not child:
            continue

        if node in nodes:
            continue

        nodes.append(child)

    return nodes


def getFrameRange():
    """Get the current frame range in Maya.

    Returns:
        tuple: A tuple containing the start and end frame numbers.
    """

    from maya import cmds

    frameRange = (
        int(cmds.playbackOptions(query=True, animationStartTime=True)),  # Get the starting frame
        int(cmds.playbackOptions(query=True, animationEndTime=True)),  # Get the ending frame
    )

    # Return the frame range as a tuple
    return frameRange


def getCameraTransforms():
    """Retrieve the names of all camera objects in the current scene.

    Returns:
        list: List of camera object names.
    """

    from maya import mel
    from maya import cmds

    # Create a list of camera names in the scene
    cameraList = cmds.ls(mel.eval("listTransforms -cameras"), long=True)

    # Return the list of camera names
    return cameraList


def getNodeName(longName):
    """Retrieves the short name of a node in Maya, stripping namespaces if present.

    This function takes a long node name as input, verifies the node's existence
    in the Maya scene, and returns its short name without any namespace prefixes.
    If the node does not exist, a warning is displayed.

    Args:
        longName (str): The full name of the Maya node, potentially including namespaces.

    Returns:
        str or None: The short name of the node without namespaces if found,
                     or None if the node does not exist in the scene.
    """

    from maya import cmds
    from maya import OpenMaya

    # Check if the specified node exists in the scene
    if not cmds.objExists(longName):
        # Display a warning in Maya if the node is not found
        OpenMaya.MGlobal.displayWarning("Could not found %s." % longName)
        # Return None if the node does not exist
        return None

    # Retrieve the short name of the node (without any hierarchical paths)
    nodeName = cmds.ls(longName, shortNames=True)[0]

    # Check if the node name contains any namespaces (indicated by ":")
    if ":" in nodeName:
        # Strip namespaces by splitting at ":" and keeping only the base name
        nodeName = nodeName.rsplit(":", nodeName.count(":"))[0]

    # Return the processed node name without namespaces
    return nodeName


def exportFbx(localPath, filename, node, frameStart, frameEnd):
    """Export selected objects to an FBX file.

    Args:
        localPath (str): The directory to save the FBX file.
        filename (str): The name of the FBX file (without extension).
        node (str): The name of the node to export.
        frameStart (int): The start frame for the animation.
        frameEnd (int): The end frame for the animation.

    Returns:
        dict: A dictionary containing the export file path, node, and frame range.
    """

    from maya import cmds

    # File extension for FBX
    extention = "fbx"

    # Construct the full file path for the FBX export
    filepath = os.path.abspath(os.path.join(localPath, "%s.%s" % (filename, extention))).replace(
        "\\", "/"
    )

    # Select the objects for export
    cmds.select(node, replace=True)

    # Perform the FBX export operation with specified settings
    cmds.file(
        filepath,
        force=True,
        options="v=0;",
        type="FBX export",
        preserveReferences=True,
        exportSelected=True,
    )

    # Deselect all objects after the export
    cmds.select(clear=True)

    # Prepare the result with file path, node name, and frame range
    result = {
        "filepath": filepath,
        "node": node,
        "frameRange": (frameStart, frameEnd),
    }

    # Return the result of the export
    return result


def exportAlembic(localPath, filename, node, frameStart, frameEnd):
    """Export selected objects to an Alembic file.

    This function exports the specified node's selected objects into an Alembic
    file format (.abc) for animation or rendering purposes.

    Args:
        localPath (str): The directory to save the Alembic file.
        filename (str): The name of the Alembic file (without extension).
        node (str): The name of the node to export.
        frameStart (int): The start frame for the animation.
        frameEnd (int): The end frame for the animation.

    Returns:
        dict: A dictionary containing the export file path, node, and frame range.
              Returns an empty dictionary if the export fails.
    """

    from maya import OpenMaya

    # File extension for Alembic
    extention = "abc"

    # Construct the full file path for the Alembic export
    filepath = os.path.abspath(os.path.join(localPath, "%s.%s" % (filename, extention))).replace(
        "\\", "/"
    )

    # Define attributes to include in export, such as metadata
    attributes = " -attr metadata"

    # Construct the MEL command for Alembic export
    melCommand = (
        'AbcExport -j "-frameRange %s %s %s -stripNamespaces -uvWrite -worldSpace -dataFormat %s -root %s -file %s";'
        % (
            frameStart,
            frameEnd,
            attributes,
            "ogawa",
            node,
            filepath,
        )
    )

    # Display the constructed export command as a warning in Maya for debugging
    OpenMaya.MGlobal.displayWarning("export command: %s" % melCommand)

    # Execute the MEL command to perform the export
    OpenMaya.MGlobal.executeCommand(melCommand, True, True)

    # Prepare the result with file path, node name, and frame range
    result = {"filepath": filepath, "node": node, "frameRange": (frameStart, frameEnd)}

    # Return the result of the export
    return result


def exportUsd(localPath, filename, node, frameStart, frameEnd):
    """Export selected objects to a USD file.

    This function exports the specified node's selected objects into a USD file
    format (.usda) for use in various 3D applications.

    Args:
        localPath (str): The directory to save the USD file.
        filename (str): The name of the USD file (without extension).
        node (str): The name of the node to export.
        frameStart (int): The start frame for the animation.
        frameEnd (int): The end frame for the animation.

    Returns:
        dict: A dictionary containing the export file path, node, and frame range.
              Returns an empty dictionary if the export fails.
    """

    from maya import cmds

    # File extension for USD
    extention = "usd"

    # Define export parameters for USD with detailed settings
    parameters = {
        "exportUVs": 1,
        "exportSkels": "none",
        "exportSkin": "none",
        "exportBlendShapes": 0,
        "exportDisplayColor": 0,
        "exportColorSets": 1,
        "exportComponentTags": 1,
        "defaultMeshScheme": "catmullClark",
        "animation": 1,
        "eulerFilter": 1,
        "staticSingleSample": 0,
        "startTime": 1001,  # Start frame for export
        "endTime": 1046,  # End frame for export
        "frameStride": 1,  # Step between frames
        "frameSample": 0.0,  # Frame sampling rate
        "defaultUSDFormat": "usda",  # USD file format
        "parentScope": "",
        "shadingMode": "useRegistry",
        "convertMaterialsTo": [],
        "exportRelativeTextures": "automatic",
        "exportInstances": 1,
        "exportVisibility": 1,
        "mergeTransformAndShape": 1,
        "stripNamespaces": 0,
        "worldspace": 0,
    }

    # Combine export parameters into a string format expected by Maya
    options = ";".join(["%s=%s" % (k, v) for k, v in parameters.items()])

    # Construct the full file path for the USD export
    filepath = os.path.abspath(os.path.join(localPath, "%s.%s" % (filename, extention))).replace(
        "\\", "/"
    )

    # Select the objects for export
    cmds.select(node, replace=True)

    # Execute the export command, with options to preserve references and force overwrite
    cmds.file(
        filepath,
        force=True,
        options=options,
        type="USD Export",
        preserveReferences=True,
        exportSelected=True,
    )

    # Deselect all objects after the export
    cmds.select(clear=True)

    # Prepare the result with file path, node name, and frame range
    result = {"filepath": filepath, "node": node, "frameRange": (frameStart, frameEnd)}

    # Return the result of the export
    return result


if __name__ == "__main__":
    pass
