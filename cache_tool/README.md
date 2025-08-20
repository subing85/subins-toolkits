https://subing85.github.io/

 Motion-Craft CACHE Tool 0.0.1
 Version: 0.0.1

A free tool designed to export Alembic and USD cache files directly from Maya or Blender scenes.

Features

    > Export geometry cache files from Maya or Blender scenes.
    > Supports both Alembic and USD cache formats.
    > Export cameras in FBX format.
    > Flexible frame range management.
    > Automatic versioning of cache files based on the scene file.
    > Customizable export with the ability to filter geometries via Python scripts.
    > Available as a standalone tool.


Tutorials

    > Tutorials and documentation will be available soon.

How to run?

    Clone or Download the tool from below link
        https://github.com/subins-toolkits/cache_tool

    Dependency python libraries

        > PySide2
        > shiboken2

        > pyqtdarktheme
        > darkdetect
        > MarkupSafe

        > Jinja2

    set the PYTHONPATH environment paths to all above python libraries, for example
    
    In windows, set PYTHONPATH=../PySide2/5.15.2.1;../shiboken2/5.15.2.1;../pyqtdarktheme/2.1.0;../Jinja2/3.1.4;../darkdetect/0.7.1;../MarkupSafe/2.1.5;../cache_tool

    python "..\cache_tool\call.py"

    Make sure maya and blender 4+ is installed

    In Project Settings,
    
        Set your project directory
        Set maya installed directory
        Set blender installed directory

    Use add button or drag and drop the maya and blender files. Select the each item and set the cache properties and save it
    
    Then Publish the cache.


    To query the right geometries, edit the class called
    
        > script.blender.ImportSource
        > script.maya.ImportSource

