def show_window():
    from smartDeformer_maya2018.resources.ui import main
    my_window = main.MainWindow()
    if not my_window:
        return
    my_window.show()
