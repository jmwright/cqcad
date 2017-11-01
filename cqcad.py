#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CQCad GUI entry point

Sets up the CQCad GUI for use - Pulls settings and populates menus.

License: LGPL 3.0
"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, qApp, QMessageBox, QMenu
from PyQt5.QtGui import QIcon
from _version import __version__

class CQCADGui(QMainWindow):
    script1stAct = None
    mouse1stAct = None
    genAct = None

    def __init__(self):
        super(CQCADGui, self).__init__()

        self.initUI()


    def clickAbout(self):
        """
        Displays a dialog with information about this application, including
        the version information for all libraries.

        :return: None
        """
        QMessageBox.about(self, "About CQCad", "CQCad 2D/3D CAD\r\nVersion: " + __version__ + "\r\n\r\nCadQuery Version: N/A\r\nPythonOCC Version: N/A\r\nFreeCAD Version: N/A")


    def notImplemented(self):
        """
        Displays a dialog with information about this application, including
        the version information for all libraries.

        :return: None
        """
        QMessageBox.about(self, "Not Implemented", "This feature has not been implemented yet. If you would like to see this feature in the release version, please vote on the GitHub repository.")


    def switchModes(self):
        """
        Toggles the other mode check menu items so that only one mode is active
        at a time.

        :return: None
        """
        sending_button = self.sender()

        # Toggle all the other items that were not selected
        if sending_button.objectName() == 'mouse_first':
            self.script1stAct.setChecked(False)
            self.genAct.setChecked(False)
        elif sending_button.objectName() == 'script_first':
            self.mouse1stAct.setChecked(False)
            self.genAct.setChecked(False)
        else:
            self.mouse1stAct.setChecked(False)
            self.script1stAct.setChecked(False)


    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('CQCad')
        self.setWindowIcon(QtGui.QIcon('content/images/compass.svg'))
        self.statusBar().showMessage('Ready')

        # Set up our menu
        exitAct = QAction(QIcon('content/images/Material/ic_exit_to_app_24px.svg'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        newProjAct = QAction('&New Project', self)
        # newProjAct.setShortcut('Ctrl+Q')
        newProjAct.setStatusTip('New project')
        newProjAct.triggered.connect(self.notImplemented)

        openProjAct = QAction('&Open Project', self)
        # openProjAct.setShortcut('Ctrl+Q')
        openProjAct.setStatusTip('Open project')
        openProjAct.triggered.connect(self.notImplemented)

        closeProjAct = QAction('&Close Project', self)
        # closeProjAct.setShortcut('Ctrl+Q')
        closeProjAct.setStatusTip('Close project')
        closeProjAct.triggered.connect(self.notImplemented)

        importAct = QAction('&Import', self)
        # importAct.setShortcut('Ctrl+Q')
        importAct.setStatusTip('Import')
        importAct.triggered.connect(self.notImplemented)

        exportAct = QAction('&Export', self)
        # exportAct.setShortcut('Ctrl+Q')
        exportAct.setStatusTip('Export')
        exportAct.triggered.connect(self.notImplemented)

        aboutAct = QAction(QIcon('content/images/Material/ic_help_24px.svg'), '&About', self)
        aboutAct.setShortcut('F1')
        aboutAct.setStatusTip('About')
        aboutAct.triggered.connect(self.clickAbout)

        execAct = QAction(QIcon('content/images/Material/ic_play_arrow_24px.svg'), '&Execute', self)
        execAct.setShortcut('F2')
        execAct.setStatusTip('Execute script')
        execAct.triggered.connect(self.notImplemented)

        debugAct = QAction(QIcon('content/images/Material/ic_bug_report_24px.svg'), '&Debug', self)
        debugAct.setShortcut('F5')
        debugAct.setStatusTip('Debug script')
        debugAct.triggered.connect(self.notImplemented)

        validAct = QAction(QIcon('content/images/Material/ic_check_circle_24px.svg'), '&Validate', self)
        validAct.setShortcut('F6')
        validAct.setStatusTip('Validate script')
        validAct.triggered.connect(self.notImplemented)

        self.mouse1stAct = QAction('&Mouse First', self, checkable=True)
        # self.mouse1stAct.setShortcut('F6')
        self.mouse1stAct.setStatusTip('Mouse first')
        self.mouse1stAct.setChecked(True)
        self.mouse1stAct.setObjectName('mouse_first')
        self.mouse1stAct.triggered.connect(self.switchModes)

        self.script1stAct = QAction('&Script First', self, checkable=True)
        # self.script1stAct.setShortcut('F6')
        self.script1stAct.setStatusTip('Script first')
        self.script1stAct.setChecked(False)
        self.script1stAct.setObjectName('script_first')
        self.script1stAct.triggered.connect(self.switchModes)

        self.genAct = QAction('&Generative', self, checkable=True)
        # self.genAct.setShortcut('F6')
        self.genAct.setStatusTip('Generative')
        self.genAct.setChecked(False)
        self.genAct.setObjectName('generative')
        self.genAct.triggered.connect(self.switchModes)

        paramsAct = QAction('&Parameters Editor', self, checkable=True)
        # paramsAct.setShortcut('F6')
        paramsAct.setStatusTip('Parameters editor')
        paramsAct.setChecked(False)
        paramsAct.setObjectName('parameters_editor')
        paramsAct.triggered.connect(self.notImplemented)

        objectAct = QAction('&Object Viewer', self, checkable=True)
        # objectAct.setShortcut('F6')
        objectAct.setStatusTip('Object viewer')
        objectAct.setChecked(False)
        objectAct.setObjectName('object_viewer')
        objectAct.triggered.connect(self.notImplemented)

        pythonAct = QAction('&Python Console', self, checkable=True)
        # pythonAct.setShortcut('F6')
        pythonAct.setStatusTip('Python console')
        pythonAct.setChecked(False)
        pythonAct.setObjectName('python_console')
        pythonAct.triggered.connect(self.notImplemented)

        extrasAct = QAction('&Extras', self)
        # extrasAct.setShortcut('F6')
        extrasAct.setStatusTip('Extras')
        extrasAct.triggered.connect(self.notImplemented)

        prefsAct = QAction('&Preferences', self)
        # prefsAct.setShortcut('F6')
        prefsAct.setStatusTip('Preferences')
        prefsAct.triggered.connect(self.notImplemented)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newProjAct)
        fileMenu.addAction(openProjAct)
        fileMenu.addAction(closeProjAct)
        recentMenu = QMenu('Recent', self)
        fileMenu.addMenu(recentMenu)
        examplesMenu = QMenu('Examples', self)
        fileMenu.addMenu(examplesMenu)
        fileMenu.addSeparator()
        fileMenu.addAction(importAct)
        fileMenu.addAction(exportAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)
        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(extrasAct)
        editMenu.addAction(prefsAct)
        viewMenu = menubar.addMenu('&View')
        modesMenu = QMenu('Modes', self)
        viewMenu.addMenu(modesMenu)
        modesMenu.addAction(self.mouse1stAct)
        modesMenu.addAction(self.script1stAct)
        modesMenu.addAction(self.genAct)
        panelsMenu = QMenu('Panels', self)
        panelsMenu.addAction(paramsAct)
        panelsMenu.addAction(objectAct)
        panelsMenu.addAction(pythonAct)
        viewMenu.addMenu(panelsMenu)
        # projMenu = menubar.addMenu('&Project')
        scriptMenu = menubar.addMenu('&Script')
        scriptMenu.addAction(execAct)
        scriptMenu.addAction(debugAct)
        scriptMenu.addAction(validAct)
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutAct)

        # # Create a central Widgets
        # centralWidget = QtGui.QWidget()
        #
        # # Create a Layout for the central Widget
        # centralLayout = QtGui.QHBoxLayout()

        self.showMaximized()


def main():
    app = QApplication(sys.argv)
    cqcad = CQCADGui()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()