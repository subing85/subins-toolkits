# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, import and export cache maya scene source code.


from __future__ import absolute_import

import os

from . import utils


class ImportSource(object):
    """Class for importing source files and managing node operations in Blender.

    Attributes:
        input (dict): A dictionary to hold input parameters for the import operation.
        output (dict): A dictionary to store output results after execution.
    """

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        """Executes the import operation for the specified Maya file.

        This method retrieves the file path, default nodes, and node names from
        the input dictionary, retrieves the corresponding nodes from Blender,
        and obtains the frame range for the animation. It then stores the
        collected information in the output dictionary.

        The input dictionary should contain the following keys:
            - "filepath": The path to the Maya file to be imported.
            - "defaultNodes": A list of default nodes to be considered.
            - "nodeNames": A list of specific node names to retrieve.

        The output dictionary will contain the following structure:
            - "result": A dictionary with the following keys:
                - "nodes": A list of retrieved node objects.
                - "frameStart": The starting frame of the animation.
                - "frameEnd": The ending frame of the animation.

        Raises:
            KeyError: If the expected keys are not found in the input dictionary.
        """

        # Retrieve the input parameters from the class dictionary
        filepath = cls.input["filepath"]  # Path to the Maya fi
        defaultNodes = cls.input["defaultNodes"]  # List of default nodes
        nodeNames = cls.input["nodeNames"]  # List of specific node names

        # Open the specified Blender scene
        utils.openScene(filepath)

        # Get nodes based on provided names and default nodes
        nodes = utils.getNodes(nodeNames=nodeNames, defaultNodes=defaultNodes)

        # Get the frame range for the current animation
        frameRange = utils.getFrameRange()

        # Prepare the output collection with nodes and frame range
        collections = {
            "nodes": nodes,  # Collected nodes
            "frameStart": frameRange[0],  # Start frame of the animation
            "frameEnd": frameRange[1],  # End frame of the animation
        }

        # Store the result in the output dictionary
        cls.output = {"result": collections}


class ExportCache(object):
    """Class for exporting cache files (Alembic, USD, FBX) from Blender.

    Attributes:
        input (dict): A dictionary to hold input parameters for the export operation.
        output (dict): A dictionary to store output results after execution.
    """

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        """Executes the export operation for the specified cache files.

        This method retrieves input parameters for file paths, frame range, cache type,
        camera settings, and node names from the input dictionary. It then sets up
        the necessary parameters, loads plugins, and performs exports based on the
        specified cache types (Alembic, USD, FBX).

        The input dictionary should contain the following keys:
            - "filepath": The path where the cache files will be saved.
            - "frameStart": The starting frame for the export.
            - "frameEnd": The ending frame for the export.
            - "cache": An integer representing the type of cache to export.
            - "cameraFBX": A boolean indicating whether to export the camera as FBX.
            - "nodes": A list of node names to export (e.g., ['scahin_models', 'ball_models', 'bat_geometrys']).
            - "localPath": The local directory path for saving cache files.

        Additional optional keys:
            - "axis": The axis to consider for exports (default is "y").
            - "fps": The frame rate setting (default is "film").
            - "unit": The unit of measurement (default is "centimeter").
            - "angle": The angle unit (default is "degree").

        The output dictionary will contain the following structure:
            - "result": A dictionary with the following keys:
                - "outputs": A list of dictionaries containing results from each export.
                - "localPath": The local path where the cache files were saved.

        Raises:
            KeyError: If the expected keys are not found in the input dictionary.
        """

        # Retrieve input parameters from the class dictionary
        filepath = cls.input["filepath"]  # Path to save cache files
        frameStart = cls.input["frameStart"]  # Start frame for export
        frameEnd = cls.input["frameEnd"]  # End frame for export
        cache = cls.input["cache"]  # Cache type (0-6)
        cameraFBX = cls.input["cameraFBX"]  # Boolean for camera FBX export
        # List of nodes to export, example ['scahin_models', 'ball_models', 'bat_geometrys']
        nodes = cls.input["nodes"]
        localPath = cls.input["localPath"]  # Local directory path for cache files

        # Get optional parameters with default values
        axis = cls.input.get("axis") or "y"  # Default axis is "y"
        time = cls.input.get("fps") or "film"  # Default time is "film"
        unit = cls.input.get("unit") or "centimeter"  # Default unit is "centimeter"
        angle = cls.input.get("angle") or "degree"  # Default angle is "degree"

        # Load necessary plugins for exporting
        utils.loadPlugins()

        # Set up startup values for the export
        startupValues = {"axis": axis, "unit": unit, "angle": angle, "time": time}
        utils.setStartup(**startupValues)

        # Open the specified Blender scene
        utils.openScene(filepath)

        # Get the current camera transforms
        cameraList = utils.getCameraTransforms()

        cachedList = list()  # List to hold export results
        nodeNames = list()  # List to keep track of processed node names

        # Loop through each node to perform exports
        for node in nodes:
            # Get the node name
            nodeName = utils.getNodeName(node)

            if not nodeName:  # Skip if the node name is not valid
                continue

            # Ensure unique node names by appending a count if necessary
            if nodeName in nodeNames:
                nodeName = "%s_%s" % (nodeName, len(nodeNames))

            # Create local path directory if it does not exist
            if not os.path.isdir(localPath):
                os.makedirs(localPath)

            # Flag to track if FBX export was performed
            isFbxExport = False

            # Initialize the result dictionary for this node
            result = dict()

            # Check if the node is a camera and export as FBX if specified
            if node in cameraList and cameraFBX:
                result = utils.exportFbx(localPath, nodeName, node, frameStart, frameEnd)
                # Append the export result
                cachedList.append(result)
                isFbxExport = True

            # Export based on the cache type

            # Alembic export conditions
            if cache in [0, 3, 5, 6]:
                # Alembic export
                result = utils.exportAlembic(localPath, nodeName, node, frameStart, frameEnd)
                cachedList.append(result)

            # USD export conditions
            if cache in [1, 3, 4, 6]:
                # Usd export
                result = utils.exportUsd(localPath, nodeName, node, frameStart, frameEnd)
                cachedList.append(result)

            # FBX export if not already done
            if cache in [2, 4, 5, 6] and not isFbxExport:
                # FBX export
                result = utils.exportFbx(localPath, nodeName, node, frameStart, frameEnd)
                cachedList.append(result)

            # Add the final result for this node
            cachedList.append(result)

            # Track processed node names
            nodeNames.append(nodeName)

        # Store the results in the output dictionary
        cls.output = {"result": {"outputs": cachedList, "localPath": localPath}}


if __name__ == "__main__":
    pass
