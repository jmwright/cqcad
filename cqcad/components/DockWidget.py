from PyQt5.QtWidgets import QDockWidget

class DockWidget(QDockWidget):
    def __init__(self, parent):
        # super(DockWidget, self).__init__()
        QDockWidget.__init__(self, "Dock", parent)

        self.initUI()

    def initUI(self):
        pass

    def closeEvent(self, event):
        """
        Allows us to clean up after ourselves and make sure that everything is
        saved that the user intended to save.

        :param event: Object describing this event
        :return: None
        """

        self.parent().uncheckDockMenu()

