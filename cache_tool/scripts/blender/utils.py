# Copyright (c) 2025, Motion-Craft Technology All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Description: Motion-Craft CACHE Tool, scripts utils source code.


from __future__ import absolute_import

import os
import sys
import logging

# Configure logging settings for tracking progress and errors
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - Line: %(lineno)d - %(message)s",
    datefmt="%Y/%m/%d %I:%M:%S %p",
    stream=sys.stdout,
)

# Create a logger instance for this module
LOGGER = logging.getLogger(__name__)


def loadPlugins():
    """Load specified plugins into Blender.

    This function enables the plugins defined in the `plugins` list.
    Any errors during loading will be logged as warnings.

    """

    import bpy

    # List of addon names to load
    plugins = list()
    # Addons example ["pose_library", "io_shape_mdd", "rigify", "add_camera_rigs", "animation_add_corrective_shape_key", "object_skinify",]

    for plugin in plugins:
        try:
            # Attempt to enable the plugin
            bpy.ops.preferences.addon_enable(module=plugin)
            LOGGER.info("Success, plug-in loaded %s" % plugin)
        except Exception as error:
            # Log any errors during loading
            LOGGER.warning(str(error))


def setStartup(*args, **kwargs):
    """Set the startup configuration for Blender.

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

    # Indicate successful execution
    return True


def openScene(filepath, **kwargs):
    """Open a Blender scene file.

    Args:
        filepath (str): The path to the .blend file to open.
        **kwargs: Additional parameters to modify the opening behavior.

    Returns:
        bool: True if the scene is opened successfully, None otherwise.
    """

    import bpy

    # Parameters for opening the scene file
    parameter = {
        "display_type": "DEFAULT",
        "sort_method": "DEFAULT",
        "load_ui": True,
        "use_scripts": True,
        "display_file_selector": True,
        "state": 0,
    }
    # Update parameters with any additional kwargs
    parameter.update(kwargs)

    # Open the scene and check if successful
    open_scene = bpy.ops.wm.open_mainfile(filepath=filepath, **kwargs)

    if "FINISHED" not in open_scene:
        return None  # Return None if the operation failed

    # Return True if the scene opened successfully
    return True


def getNodes(**kwargs):
    """Retrieve nodes from the current Blender scene.

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

    import bpy

    # Get the active scene collection
    sceneCollection = bpy.context.scene.collection

    nodes = list()

    # Check all objects in the scene for matching node names
    for object in sceneCollection.all_objects:
        for name in nodeNames:
            if name.lower() not in object.name.lower():
                continue
            # Add matching object name to the list
            nodes.append(object.name)
            break

    # Check child collections for matching node names
    for collection in sceneCollection.children_recursive:
        for name in nodeNames:
            if name.lower() not in collection.name.lower():
                continue
            # Add matching collection name to the list
            nodes.append(collection.name)
            break

    # Return the list of found node names
    return nodes


def getFrameRange():
    """Get the current frame range in Blender.

    Returns:
        tuple: A tuple containing the start and end frame numbers.
    """

    import bpy

    frameRange = (
        int(bpy.context.scene.frame_start),  # Get the starting frame
        int(bpy.context.scene.frame_end),  # Get the ending frame
    )

    # Return the frame range as a tuple
    return frameRange


def getCameraTransforms():
    """Retrieve the names of all camera objects in the current scene.

    Returns:
        list: List of camera object names.
    """

    import bpy

    # Create a list of camera names in the scene
    cameraList = [object.name for object in bpy.context.scene.objects if object.type == "CAMERA"]

    # Return the list of camera names
    return cameraList


def getNodeName(name):
    """Get the node name from the collection or object.

    Args:
        name (str): The name of the node to find.

    Returns:
        str or None: The node name with periods replaced by underscores, or None if not found.
    """

    import bpy

    # Try to get the collection
    result = bpy.data.collections.get(name)

    # If the collection doesn't exist, try to get the object
    if not result:
        # Get the object from the collection
        result = bpy.data.objects.get(name)

    if not result:
        # Log a warning if not found
        LOGGER.warning("Could not found %s." % name)
        return None  # Return None if neither collection nor object is found

    # Format the node name for consistency
    if "." in result.name:
        # nodeName = nodeName.rsplit(".", nodeName.count(":"))[0]
        nodeName = result.name.replace(".", "_")  # Replace '.' with '_'
    else:
        nodeName = result.name

    # Return the formatted node name
    return nodeName


def getObjects(name):
    """Get all objects in a specified collection or a single object.

    Args:
        name (str): The name of the collection or object.

    Returns:
        list: List of objects in the collection or the specified object with its children.
    """

    import bpy

    # Get the collection by name
    collection = bpy.data.collections.get(name)

    if collection:
        # Return all objects in the collection
        return collection.all_objects

    # Try to get the object by name
    object = bpy.data.objects.get(name)

    # Return the object and its children
    return [object] + object.children_recursive


def selectObject(objects):
    """Select specified objects in Blender.

    Args:
        objects (list): List of object names or Blender objects to select.
    """

    import bpy

    # Deselect all objects
    bpy.ops.object.select_all(action="DESELECT")

    for object in objects:
        if isinstance(object, str):
            # Get the object by name if a string
            object = bpy.data.objects.get(object)

        # Set the object as active
        bpy.context.view_layer.objects.active = object

        # Select the object
        object.select_set(True)


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

    import bpy

    # File extension for FBX
    extention = "fbx"

    # Construct the full file path for the FBX export
    filepath = os.path.abspath(os.path.join(localPath, "%s.%s" % (filename, extention))).replace(
        "\\", "/"
    )

    # Get objects to export based on the specified node
    objects = getObjects(node)

    # Select the objects for export
    selectObject(objects)

    # Perform the FBX export operation with specified settings
    fbxExport = bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=True,
        bake_anim=True,
        bake_anim_use_all_bones=True,
        bake_anim_use_nla_strips=True,
        bake_anim_use_all_actions=True,
        bake_anim_force_startend_keying=True,
        bake_anim_step=1.0,
        bake_anim_simplify_factor=1.0,
        check_existing=True,
        filter_glob="*.fbx",
        use_visible=False,
        use_active_collection=False,
        # collection="",
        global_scale=1.0,
        apply_unit_scale=True,
        apply_scale_options="FBX_SCALE_NONE",
        use_space_transform=True,
        bake_space_transform=False,
        object_types={"ARMATURE", "CAMERA", "EMPTY", "LIGHT", "MESH", "OTHER"},
        use_mesh_modifiers=True,
        use_mesh_modifiers_render=True,
        mesh_smooth_type="OFF",
        colors_type="SRGB",
        prioritize_active_color=False,
        use_subsurf=False,
        use_mesh_edges=False,
        use_tspace=False,
        use_triangles=False,
        use_custom_props=False,
        add_leaf_bones=True,
        primary_bone_axis="Y",
        secondary_bone_axis="X",
        use_armature_deform_only=False,
        armature_nodetype="NULL",
        path_mode="AUTO",
        embed_textures=False,
        batch_mode="OFF",
        use_batch_own_dir=True,
        use_metadata=True,
        axis_forward="-Z",
        axis_up="Y",
    )

    # Deselect all objects after the export
    bpy.ops.object.select_all(action="DESELECT")

    # Check if the export operation was successful
    if "FINISHED" not in fbxExport:
        # Return an empty dictionary if export failed
        return dict()

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

    import bpy

    # File extension for Alembic
    extention = "abc"

    # Construct the full file path for the Alembic export
    filepath = os.path.abspath(os.path.join(localPath, "%s.%s" % (filename, extention))).replace(
        "\\", "/"
    )

    # Get objects to export based on the specified node
    objects = getObjects(node)

    # Select the objects for export
    selectObject(objects)

    # Perform the Alembic export operation with specified settings
    alembicExport = bpy.ops.wm.alembic_export(
        filepath=filepath,
        start=frameStart,
        end=frameEnd,
        init_scene_frame_range=True,
        selected=True,
        # collection="",
        check_existing=True,
        filter_blender=False,
        filter_backup=False,
        filter_image=False,
        filter_movie=False,
        filter_python=False,
        filter_font=False,
        filter_sound=False,
        filter_text=False,
        filter_archive=False,
        filter_btx=False,
        filter_collada=False,
        filter_alembic=True,
        filter_usd=False,
        filter_obj=False,
        filter_volume=False,
        filter_folder=True,
        filter_blenlib=False,
        filemode=8,
        display_type="DEFAULT",
        sort_method="DEFAULT",
        filter_glob="*.abc",
        xsamples=1,
        gsamples=1,
        sh_open=0.0,
        sh_close=1.0,
        visible_objects_only=False,
        flatten=False,
        uvs=True,
        packuv=True,
        normals=True,
        vcolors=False,
        orcos=True,
        face_sets=False,
        subdiv_schema=False,
        apply_subdiv=False,
        curves_as_mesh=False,
        use_instancing=True,
        global_scale=1.0,
        triangulate=False,
        quad_method="SHORTEST_DIAGONAL",
        ngon_method="BEAUTY",
        export_hair=True,
        export_particles=True,
        export_custom_properties=True,
        as_background_job=False,
        evaluation_mode="RENDER",
    )

    # Deselect all objects after the export
    bpy.ops.object.select_all(action="DESELECT")

    # Check if the export operation was successful
    if "FINISHED" not in alembicExport:
        # Return an empty dictionary if export failed
        return dict()

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

    import bpy

    # File extension for USD
    extention = "usda"

    # Construct the full file path for the USD export
    filepath = os.path.abspath(os.path.join(localPath, "%s.%s" % (filename, extention))).replace(
        "\\", "/"
    )

    # Get objects to export based on the specified node
    objects = getObjects(node)

    # Select the objects for export
    selectObject(objects)

    # Perform the USD export operation with specified settings
    usdExport = bpy.ops.wm.usd_export(
        filepath=filepath,
        selected_objects_only=True,
        export_animation=True,
        # frame_start=frameStart,
        # frame_end=frameEnd,
        check_existing=True,
        filter_blender=False,
        filter_backup=False,
        filter_image=False,
        filter_movie=False,
        filter_python=False,
        filter_font=False,
        filter_sound=False,
        filter_text=False,
        filter_archive=False,
        filter_btx=False,
        filter_collada=False,
        filter_alembic=False,
        filter_usd=True,
        filter_obj=False,
        filter_volume=False,
        filter_folder=True,
        filter_blenlib=False,
        filemode=8,
        display_type="DEFAULT",
        sort_method="DEFAULT",
        filter_glob="*.usda",
        visible_objects_only=True,
        # collection="",
        export_hair=True,
        export_uvmaps=True,
        # rename_uvmaps=True,
        export_mesh_colors=True,
        export_normals=True,
        export_materials=True,
        # export_subdivision="BEST_MATCH",
        # export_armatures=True,
        # only_deform_bones=False,
        # export_shapekeys=True,
        use_instancing=False,
        evaluation_mode="RENDER",
        generate_preview_surface=True,
        # generate_materialx_network=False,
        # convert_orientation=False,
        # export_global_forward_selection="NEGATIVE_Z",
        # export_global_up_selection="Y",
        export_textures=True,
        overwrite_textures=False,
        relative_paths=True,
        # xform_op_mode="TRS",
        root_prim_path="",
        # export_custom_properties=True,
        # custom_properties_namespace="userProperties",
        # author_blender_name=True,
        # convert_world_material=True,
        # allow_unicode=False,
        # export_meshes=True,
        # export_lights=True,
        # export_cameras=True,
        # export_curves=True,
        # export_volumes=True,
        # triangulate_meshes=False,
        # quad_method="SHORTEST_DIAGONAL",
        # ngon_method="BEAUTY",
        # usdz_downscale_size="KEEP",
        # usdz_downscale_custom_size=128,
    )

    # Deselect all objects after the export
    bpy.ops.object.select_all(action="DESELECT")

    # Check if the export operation was successful
    if "FINISHED" not in usdExport:
        # Return an empty dictionary if export failed
        return dict()

    # Rename the file from .usda to .usd
    newfilepath = os.path.abspath("%s.usd" % os.path.splitext(filepath)[0]).replace("\\", "/")
    os.rename(filepath, newfilepath)

    # Prepare the result with file path, node name, and frame range
    result = {"filepath": newfilepath, "node": node, "frameRange": (frameStart, frameEnd)}

    # Return the result of the export
    return result


if __name__ == "__main__":
    pass
