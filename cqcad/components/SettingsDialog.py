from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QCheckBox

class SettingsDialog(QDialog):
    settings = QSettings('cqcad', 'settings')

    def __init__(self):
        super(SettingsDialog, self).__init__()

        self.layout = QVBoxLayout(self)

        self.resize(600, 400)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Python Editor")
        self.tabs.addTab(self.tab2, "CAD Engine")

        # Set up first tab
        self.tab1.layout = QVBoxLayout(self)

        # Line numbers checkbox
        self.lineNumbersCB = QCheckBox('Show Line Numbers', self)
        lineNumbersCheckedState = self.settings.value('editor_line_numbers_visible', type=bool)
        self.lineNumbersCB.setChecked(lineNumbersCheckedState)
        self.lineNumbersCB.stateChanged.connect(self.changeLineNumberSetting)

        self.tab1.layout.addWidget(self.lineNumbersCB)
        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        # self.setLayout(self.layout)

        self.setWindowTitle("CQCad Settings")
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

        # TODO: Init with keybindings, execute_on_save, use_external_editor, max_line_length settings, line_numbers, cad_engine

    def changeLineNumberSetting(self):
        """
        Changes the setting for whether or not line numbers are enabled on the Python editor
        :return: None
        """

        self.settings.setValue('editor_line_numbers_visible', self.sender().isChecked())

    def closeEvent(self, event):
        """
        Allows us to clean up after ourselves and make sure that everything is
        saved that the user intended to save.

        :param event: Object describing this event
        :return: None
        """

        self.settings.sync()