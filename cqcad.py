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
        varTitle = QtCore.QCoreApplication.translate('cqcad', "About CQCad")
        varMsg = QtCore.QCoreApplication.translate('cqcad', "CQCad 2D/3D CAD\r\nVersion: " + __version__ + "\r\n\r\nCadQuery Version: N/A\r\nPythonOCC Version: N/A\r\nFreeCAD Version: N/A")

        QMessageBox.about(self, varTitle, varMsg)


    def notImplemented(self):
        """
        Displays a dialog with information about this application, including
        the version information for all libraries.

        :return: None
        """
        niTitle = "Not Implemented"
        niMsg = QtCore.QCoreApplication.translate('cqcad', "This feature has not been implemented yet. If you would like to see this feature in the release version, please create an issue on the GitHub repository. https://github.com/jmwright/cqcad")

        QMessageBox.about(self, niTitle, niMsg)


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
        # Translations of menu items
        exitName = QtCore.QCoreApplication.translate('cqcad', "Exit")
        exitTip = QtCore.QCoreApplication.translate('cqcad', "Exit application")
        nProjName = QtCore.QCoreApplication.translate('cqcad', "New Project")
        nProjTip = QtCore.QCoreApplication.translate('cqcad', "New project")
        oProjName = QtCore.QCoreApplication.translate('cqcad', "Open Project")
        oProjTip = QtCore.QCoreApplication.translate('cqcad', "Open project")
        cProjName = QtCore.QCoreApplication.translate('cqcad', "Close Project")
        cProjTip = QtCore.QCoreApplication.translate('cqcad', "Close project")
        impName = QtCore.QCoreApplication.translate('cqcad', "Import")
        impTip = QtCore.QCoreApplication.translate('cqcad', "Import")
        expName = QtCore.QCoreApplication.translate('cqcad', "Export")
        expTip = QtCore.QCoreApplication.translate('cqcad', "Export")
        abtName = QtCore.QCoreApplication.translate('cqcad', "About")
        abtTip = QtCore.QCoreApplication.translate('cqcad', "About")
        execName = QtCore.QCoreApplication.translate('cqcad', "Execute")
        execTip = QtCore.QCoreApplication.translate('cqcad', "Execute script")
        dbgName = QtCore.QCoreApplication.translate('cqcad', "Debug")
        dbgTip = QtCore.QCoreApplication.translate('cqcad', "Debug script")
        validName = QtCore.QCoreApplication.translate('cqcad', "Validate")
        validTip = QtCore.QCoreApplication.translate('cqcad', "Validate script")
        m1stName = QtCore.QCoreApplication.translate('cqcad', "Mouse First")
        m1stTip = QtCore.QCoreApplication.translate('cqcad', "Mouse first")
        s1stName = QtCore.QCoreApplication.translate('cqcad', "Script First")
        s1stTip = QtCore.QCoreApplication.translate('cqcad', "Script first")
        genName = QtCore.QCoreApplication.translate('cqcad', "Generative")
        genTip = QtCore.QCoreApplication.translate('cqcad', "Generative")
        pEdName = QtCore.QCoreApplication.translate('cqcad', "Parameters Editor")
        pEdTip = QtCore.QCoreApplication.translate('cqcad', "Parameters editor")
        viewerName = QtCore.QCoreApplication.translate('cqcad', "Object Viewer")
        viewerTip = QtCore.QCoreApplication.translate('cqcad', "Object viewer")
        conName = QtCore.QCoreApplication.translate('cqcad', "Console")
        conTip = QtCore.QCoreApplication.translate('cqcad', "Console")
        extrasName = QtCore.QCoreApplication.translate('cqcad', "Extras")
        extrastip = QtCore.QCoreApplication.translate('cqcad', "Extras")
        setsName = QtCore.QCoreApplication.translate('cqcad', "Settings")
        setsTip = QtCore.QCoreApplication.translate('cqcad', "Settings")
        fileName = QtCore.QCoreApplication.translate('cqcad', "File")
        rcntName = QtCore.QCoreApplication.translate('cqcad', "Recent")
        exName = QtCore.QCoreApplication.translate('cqcad', "Examples")
        editName = QtCore.QCoreApplication.translate('cqcad', "Edit")
        viewName = QtCore.QCoreApplication.translate('cqcad', "View")
        modesName = QtCore.QCoreApplication.translate('cqcad', "Modes")
        panelsName = QtCore.QCoreApplication.translate('cqcad', "Panels")
        scriptName = QtCore.QCoreApplication.translate('cqcad', "Script")
        helpName = QtCore.QCoreApplication.translate('cqcad', "Help")

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('CQCad')
        self.setWindowIcon(QtGui.QIcon('content/images/compass.svg'))
        self.statusBar().showMessage('Ready')

        # Set up our menu
        exitAct = QAction(QIcon('content/images/Material/ic_exit_to_app_24px.svg'), '&' + exitName, self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip(exitTip)
        exitAct.triggered.connect(qApp.quit)

        newProjAct = QAction('&' + nProjName, self)
        # newProjAct.setShortcut('Ctrl+Q')
        newProjAct.setStatusTip(nProjTip)
        newProjAct.triggered.connect(self.notImplemented)

        openProjAct = QAction('&' + oProjName, self)
        # openProjAct.setShortcut('Ctrl+Q')
        openProjAct.setStatusTip(oProjTip)
        openProjAct.triggered.connect(self.notImplemented)

        closeProjAct = QAction('&' + cProjName, self)
        # closeProjAct.setShortcut('Ctrl+Q')
        closeProjAct.setStatusTip(cProjTip)
        closeProjAct.triggered.connect(self.notImplemented)

        importAct = QAction('&' + impName, self)
        # importAct.setShortcut('Ctrl+Q')
        importAct.setStatusTip(impTip)
        importAct.triggered.connect(self.notImplemented)

        exportAct = QAction('&' + expName, self)
        # exportAct.setShortcut('Ctrl+Q')
        exportAct.setStatusTip(expTip)
        exportAct.triggered.connect(self.notImplemented)

        aboutAct = QAction(QIcon('content/images/Material/ic_help_24px.svg'), '&' + abtName, self)
        aboutAct.setShortcut('F1')
        aboutAct.setStatusTip(abtTip)
        aboutAct.triggered.connect(self.clickAbout)

        execAct = QAction(QIcon('content/images/Material/ic_play_arrow_24px.svg'), '&' + execName, self)
        execAct.setShortcut('F2')
        execAct.setStatusTip(execTip)
        execAct.triggered.connect(self.notImplemented)

        debugAct = QAction(QIcon('content/images/Material/ic_bug_report_24px.svg'), '&' + dbgName, self)
        debugAct.setShortcut('F5')
        debugAct.setStatusTip(dbgTip)
        debugAct.triggered.connect(self.notImplemented)

        validAct = QAction(QIcon('content/images/Material/ic_check_circle_24px.svg'), '&' + validName, self)
        validAct.setShortcut('F6')
        validAct.setStatusTip(validTip)
        validAct.triggered.connect(self.notImplemented)

        self.mouse1stAct = QAction('&' + m1stName, self, checkable=True)
        # self.mouse1stAct.setShortcut('F6')
        self.mouse1stAct.setStatusTip(m1stTip)
        self.mouse1stAct.setChecked(True)
        self.mouse1stAct.setObjectName('mouse_first')
        self.mouse1stAct.triggered.connect(self.switchModes)

        self.script1stAct = QAction('&' + s1stName, self, checkable=True)
        # self.script1stAct.setShortcut('F6')
        self.script1stAct.setStatusTip(s1stTip)
        self.script1stAct.setChecked(False)
        self.script1stAct.setObjectName('script_first')
        self.script1stAct.triggered.connect(self.switchModes)

        self.genAct = QAction('&' + genName, self, checkable=True)
        # self.genAct.setShortcut('F6')
        self.genAct.setStatusTip(genTip)
        self.genAct.setChecked(False)
        self.genAct.setObjectName('generative')
        self.genAct.triggered.connect(self.switchModes)

        paramsAct = QAction('&' + pEdName, self, checkable=True)
        # paramsAct.setShortcut('F6')
        paramsAct.setStatusTip(pEdTip)
        paramsAct.setChecked(False)
        paramsAct.setObjectName('parameters_editor')
        paramsAct.triggered.connect(self.notImplemented)

        objectAct = QAction('&' + viewerName, self, checkable=True)
        # objectAct.setShortcut('F6')
        objectAct.setStatusTip(viewerTip)
        objectAct.setChecked(False)
        objectAct.setObjectName('object_viewer')
        objectAct.triggered.connect(self.notImplemented)

        pythonAct = QAction('&' + conName, self, checkable=True)
        # pythonAct.setShortcut('F6')
        pythonAct.setStatusTip(conTip)
        pythonAct.setChecked(False)
        pythonAct.setObjectName('python_console')
        pythonAct.triggered.connect(self.notImplemented)

        extrasAct = QAction('&' + extrasName, self)
        # extrasAct.setShortcut('F6')
        extrasAct.setStatusTip(extrastip)
        extrasAct.triggered.connect(self.notImplemented)

        settingsAct = QAction('&' + setsName, self)
        # settingsAct.setShortcut('F6')
        settingsAct.setStatusTip(setsTip)
        settingsAct.triggered.connect(self.notImplemented)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&' + fileName)
        fileMenu.addAction(newProjAct)
        fileMenu.addAction(openProjAct)
        fileMenu.addAction(closeProjAct)
        recentMenu = QMenu(rcntName, self)
        fileMenu.addMenu(recentMenu)
        examplesMenu = QMenu(exName, self)
        fileMenu.addMenu(examplesMenu)
        fileMenu.addSeparator()
        fileMenu.addAction(importAct)
        fileMenu.addAction(exportAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)
        editMenu = menubar.addMenu('&' + editName)
        editMenu.addAction(extrasAct)
        editMenu.addAction(settingsAct)
        viewMenu = menubar.addMenu('&' + viewName)
        modesMenu = QMenu(modesName, self)
        viewMenu.addMenu(modesMenu)
        modesMenu.addAction(self.mouse1stAct)
        modesMenu.addAction(self.script1stAct)
        modesMenu.addAction(self.genAct)
        panelsMenu = QMenu(panelsName, self)
        panelsMenu.addAction(paramsAct)
        panelsMenu.addAction(objectAct)
        panelsMenu.addAction(pythonAct)
        viewMenu.addMenu(panelsMenu)
        # projMenu = menubar.addMenu('&Project')
        scriptMenu = menubar.addMenu('&' + scriptName)
        scriptMenu.addAction(execAct)
        scriptMenu.addAction(debugAct)
        scriptMenu.addAction(validAct)
        helpMenu = menubar.addMenu('&' + helpName)
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