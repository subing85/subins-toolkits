def show_window():
    from smartDeformer_maya2023.resources.ui import main

    from smartDeformer_maya2023.resources.ui import weights
    from smartDeformer_maya2023.modules import readWrite
    from smartDeformer_maya2023.utils import platforms
    from smartDeformer_maya2023.resources.ui import geometry
    from smartDeformer_maya2023.utils import generic

    import importlib

    importlib.reload(weights)
    importlib.reload(readWrite)
    importlib.reload(platforms)
    importlib.reload(geometry)
    importlib.reload(generic)
    importlib.reload(main)

    my_window = main.MainWindow()
    if not my_window:
        return
    my_window.show()
