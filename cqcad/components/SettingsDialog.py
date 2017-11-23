from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QCheckBox

class SettingsDialog(QDialog):
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
        # self.lineNumbersCB.move(20, 20)
        self.lineNumbersCB.toggle()
        self.lineNumbersCB.stateChanged.connect(self.toggleLineNumber)

        self.tab1.layout.addWidget(self.lineNumbersCB)
        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        # self.setLayout(self.layout)

        self.setWindowTitle("CQCad Settings")
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

        # TODO: Init with keybindings, execute_on_save, use_external_editor, max_line_length settings, line_numbers, cad_engine

    def toggleLineNumber(self):
        print("Toggling Line Number")

        # TODO: Start here and change the setting for the line numbers