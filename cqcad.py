#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CQCad GUI entry point

Sets up the CQCad GUI for use - Pulls settings and populates menus.

License: LGPL 3.0
"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, qApp, QMessageBox, QMenu, QDialog, QLabel, QDockWidget, QMdiArea
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSettings
from _version import __version__
from components.CodeEdit import CodeEdit


class CQCADGui(QMainWindow):
    settings = QSettings('cqcad', 'settings')       # Platform independent application settings
    guiState = QSettings('cqcad', 'gui')  # Platform independent application settings
    script1stAct = None
    mouse1stAct = None
    fileMenu = None             # The File menu
    recentMenu = None           # The recent scripts submenu
    examplesMenu = None         # The examples submenu

    def __init__(self):
        super(CQCADGui, self).__init__()

        self.initUI()


    def closeEvent(self, event):
        """
        Allows us to clean up after ourselves and make sure that everything is
        saved that the user intended to save.

        :param event: Object describing this event
        :return: None
        """

        self.guiState.sync()
        self.settings.sync()


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
        elif sending_button.objectName() == 'script_first':
            self.mouse1stAct.setChecked(False)


    def toggleDock(self):
        """
        Toggles the dock widgets visibility when the menu item is clicked.

        :return: None
        """
        if self.dock.isVisible() == True:
            self.dock.hide()
            self.dockAct.setChecked(False)

            # Keep track of the state of the GUI for the user
            self.guiState.setValue('dock_visible', False)
        else:
            self.dock.show()
            self.dockAct.setChecked(True)

            # Keep track of the state of the GUI for the user
            self.guiState.setValue('dock_visible', True)

        self.guiState.sync()


    def uncheckDockMenu(self):
        """
        Unchecks the dock menu item if the dock widget is closed manually.

        :return: None
        """
        if not self.dock.isVisible():
            self.dockAct.setChecked(False)

            # Keep track of the state of the GUI for the user
            self.guiState.setValue('dock_visible', False)

    def setInitialDockState(self):
        dockState = self.guiState.value('dock_visible', type=bool)

        if dockState:
            self.dock.show()
            self.dockAct.setChecked(True)
        else:
            self.dock.hide()
            self.dockAct.setChecked(False)


    def initUI(self):
        # Translations of menu items
        exitName = QtCore.QCoreApplication.translate('cqcad', "Exit")
        exitTip = QtCore.QCoreApplication.translate('cqcad', "Exit application")
        newName = QtCore.QCoreApplication.translate('cqcad', "New")
        newTip = QtCore.QCoreApplication.translate('cqcad', "New project or script")
        openName = QtCore.QCoreApplication.translate('cqcad', "Open")
        openTip = QtCore.QCoreApplication.translate('cqcad', "Open project or script")
        closeName = QtCore.QCoreApplication.translate('cqcad', "Close")
        closeTip = QtCore.QCoreApplication.translate('cqcad', "Close project or script")
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
        m1stName = QtCore.QCoreApplication.translate('cqcad', "Mouse First (Experimental)")
        m1stTip = QtCore.QCoreApplication.translate('cqcad', "Mouse first (experimental)")
        s1stName = QtCore.QCoreApplication.translate('cqcad', "Script First")
        s1stTip = QtCore.QCoreApplication.translate('cqcad', "Script first")
        pEdName = QtCore.QCoreApplication.translate('cqcad', "Parameters Editor")
        pEdTip = QtCore.QCoreApplication.translate('cqcad', "Parameters editor")
        viewerName = QtCore.QCoreApplication.translate('cqcad', "Object Viewer")
        viewerTip = QtCore.QCoreApplication.translate('cqcad', "Object viewer")
        conName = QtCore.QCoreApplication.translate('cqcad', "Console")
        conTip = QtCore.QCoreApplication.translate('cqcad', "Console")
        dockName = QtCore.QCoreApplication.translate('cqcad', "Dock")
        libsName = QtCore.QCoreApplication.translate('cqcad', "Collections")
        libsTip = QtCore.QCoreApplication.translate('cqcad', "Collections")
        extsName = QtCore.QCoreApplication.translate('cqcad', "Extensions")
        extsTip = QtCore.QCoreApplication.translate('cqcad', "Extensions")
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
        axioViewName = QtCore.QCoreApplication.translate('cqcad', "Axiometric View")
        axioViewTip = QtCore.QCoreApplication.translate('cqcad', "Axiometric View")
        frontViewName = QtCore.QCoreApplication.translate('cqcad', "Front View")
        frontViewTip = QtCore.QCoreApplication.translate('cqcad', "Front View")
        backViewName = QtCore.QCoreApplication.translate('cqcad', "Back View")
        backViewTip = QtCore.QCoreApplication.translate('cqcad', "Back View")
        topViewName = QtCore.QCoreApplication.translate('cqcad', "Top View")
        topViewTip = QtCore.QCoreApplication.translate('cqcad', "Top View")
        bottomViewName = QtCore.QCoreApplication.translate('cqcad', "Bottom View")
        bottomViewTip = QtCore.QCoreApplication.translate('cqcad', "Bottom View")
        leftViewName = QtCore.QCoreApplication.translate('cqcad', "Left View")
        leftViewTip = QtCore.QCoreApplication.translate('cqcad', "Left View")
        rightViewName = QtCore.QCoreApplication.translate('cqcad', "Right View")
        rightViewTip = QtCore.QCoreApplication.translate('cqcad', "Right View")
        fitAllName = QtCore.QCoreApplication.translate('cqcad', "Fit All")
        fitAllTip = QtCore.QCoreApplication.translate('cqcad', "Fit All")

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('CQCad')
        self.setWindowIcon(QtGui.QIcon('content/images/compass.svg'))
        self.statusBar().showMessage('Ready')

        # Set up our menu
        exitAct = QAction(QIcon('content/images/Material/ic_exit_to_app_24px.svg'), '&' + exitName, self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip(exitTip)
        exitAct.triggered.connect(qApp.quit)

        newAct = QAction('&' + newName, self)
        # newAct.setShortcut('Ctrl+Q')
        newAct.setStatusTip(newTip)
        newAct.triggered.connect(self.notImplemented)

        openAct = QAction('&' + openName, self)
        # openAct.setShortcut('Ctrl+Q')
        openAct.setStatusTip(openTip)
        openAct.triggered.connect(self.notImplemented)

        closeAct = QAction('&' + closeName, self)
        # closeAct.setShortcut('Ctrl+Q')
        closeAct.setStatusTip(closeTip)
        closeAct.triggered.connect(self.notImplemented)

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

        validAct = QAction(QIcon('content/images/Material/ic_check_black_24px.svg'), '&' + validName, self)
        validAct.setShortcut('F6')
        validAct.setStatusTip(validTip)
        validAct.triggered.connect(self.notImplemented)

        self.mouse1stAct = QAction('&' + m1stName, self, checkable=True)
        # self.mouse1stAct.setShortcut('F6')
        self.mouse1stAct.setStatusTip(m1stTip)
        self.mouse1stAct.setChecked(False)
        self.mouse1stAct.setObjectName('mouse_first')
        self.mouse1stAct.triggered.connect(self.switchModes)

        self.script1stAct = QAction('&' + s1stName, self, checkable=True)
        # self.script1stAct.setShortcut('F6')
        self.script1stAct.setStatusTip(s1stTip)
        self.script1stAct.setChecked(True)
        self.script1stAct.setObjectName('script_first')
        self.script1stAct.triggered.connect(self.switchModes)

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

        # Start here and link the dock view menu items with the visibility of the dock
        self.dockAct = QAction('&' + dockName, self, checkable=True)
        self.dockAct.setStatusTip(conTip)
        self.dockAct.setChecked(True)
        self.dockAct.setObjectName('dock_panel')
        self.dockAct.triggered.connect(self.toggleDock)

        libsAct = QAction('&' + libsName, self)
        # libsAct.setShortcut('F6')
        libsAct.setStatusTip(libsTip)
        libsAct.triggered.connect(self.notImplemented)

        extsAct = QAction('&' + extsName, self)
        # extsAct.setShortcut('F6')
        extsAct.setStatusTip(extsTip)
        extsAct.triggered.connect(self.notImplemented)

        frontViewAct = QAction(QIcon('content/images/front_view.svg'), '&' + frontViewName, self)
        frontViewAct.setShortcut('1')
        frontViewAct.setStatusTip(frontViewTip)
        frontViewAct.triggered.connect(self.notImplemented)

        backViewAct = QAction(QIcon('content/images/back_view.svg'), '&' + backViewName, self)
        backViewAct.setShortcut('2')
        backViewAct.setStatusTip(backViewTip)
        backViewAct.triggered.connect(self.notImplemented)

        topViewAct = QAction(QIcon('content/images/top_view.svg'), '&' + topViewName, self)
        topViewAct.setShortcut('3')
        topViewAct.setStatusTip(topViewTip)
        topViewAct.triggered.connect(self.notImplemented)

        bottomViewAct = QAction(QIcon('content/images/bottom_view.svg'), '&' + bottomViewName, self)
        bottomViewAct.setShortcut('4')
        bottomViewAct.setStatusTip(bottomViewTip)
        bottomViewAct.triggered.connect(self.notImplemented)

        leftViewAct = QAction(QIcon('content/images/left_side_view.svg'), '&' + leftViewName, self)
        leftViewAct.setShortcut('5')
        leftViewAct.setStatusTip(leftViewTip)
        leftViewAct.triggered.connect(self.notImplemented)

        rightViewAct = QAction(QIcon('content/images/right_side_view.svg'), '&' + rightViewName, self)
        rightViewAct.setShortcut('6')
        rightViewAct.setStatusTip(rightViewTip)
        rightViewAct.triggered.connect(self.notImplemented)

        axioViewAct = QAction(QIcon('content/images/axiometric_view.svg'), '&' + axioViewName, self)
        axioViewAct.setShortcut('0')
        axioViewAct.setStatusTip(axioViewTip)
        axioViewAct.triggered.connect(self.notImplemented)

        fitAllAct = QAction(QIcon('content/images/fit_all.svg'), '&' + fitAllName, self)
        # fitAllAct.setShortcut('6')
        fitAllAct.setStatusTip(fitAllTip)
        fitAllAct.triggered.connect(self.notImplemented)

        settingsAct = QAction('&' + setsName, self)
        # settingsAct.setShortcut('F6')
        settingsAct.setStatusTip(setsTip)
        settingsAct.triggered.connect(self.showSettingsDialog)

        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&' + fileName)
        self.fileMenu.addAction(newAct)
        self.fileMenu.addAction(openAct)
        self.fileMenu.addAction(closeAct)
        self.recentMenu = QMenu(rcntName, self)
        self.fileMenu.addMenu(self.recentMenu)
        self.examplesMenu = QMenu(exName, self)
        self.fileMenu.addMenu(self.examplesMenu)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(importAct)
        self.fileMenu.addAction(exportAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(exitAct)
        editMenu = menubar.addMenu('&' + editName)
        editMenu.addAction(libsAct)
        editMenu.addAction(extsAct)
        editMenu.addAction(settingsAct)
        viewMenu = menubar.addMenu('&' + viewName)
        modesMenu = QMenu(modesName, self)
        viewMenu.addMenu(modesMenu)
        modesMenu.addAction(self.mouse1stAct)
        modesMenu.addAction(self.script1stAct)
        panelsMenu = QMenu(panelsName, self)
        panelsMenu.addAction(paramsAct)
        panelsMenu.addAction(objectAct)
        panelsMenu.addAction(pythonAct)
        panelsMenu.addAction(self.dockAct)
        viewMenu.addMenu(panelsMenu)
        # projMenu = menubar.addMenu('&Project')
        scriptMenu = menubar.addMenu('&' + scriptName)
        scriptMenu.addAction(execAct)
        scriptMenu.addAction(debugAct)
        scriptMenu.addAction(validAct)
        helpMenu = menubar.addMenu('&' + helpName)
        helpMenu.addAction(aboutAct)

        # The CadQuery logo
        logoLabel = QLabel()
        logoLabel.setPixmap(QPixmap('content/images/cadquery_logo.svg'))

        # Toolbar for CAD controls and extension controls
        self.toolbar = self.addToolBar('Main Tools')
        self.toolbar.addWidget(logoLabel)
        self.toolbar.addAction(execAct)
        self.toolbar.addAction(debugAct)
        self.toolbar.addAction(validAct)
        self.toolbar.addAction(frontViewAct)
        self.toolbar.addAction(backViewAct)
        self.toolbar.addAction(topViewAct)
        self.toolbar.addAction(bottomViewAct)
        self.toolbar.addAction(leftViewAct)
        self.toolbar.addAction(rightViewAct)
        self.toolbar.addAction(axioViewAct)
        self.toolbar.addAction(fitAllAct)

        # Side dock for things like the object viewer
        self.dock = QDockWidget("Dock", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        self.dock.visibilityChanged.connect(self.uncheckDockMenu)
        self.dock.setMinimumSize(200, 100);
        self.setInitialDockState()

        # The central MDI window area
        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        # For now, default to opening a script editor
        child = CodeEdit()
        self.mdiArea.setWindowIcon(QIcon('content/images/python_logo.svg'))
        self.mdiArea.addSubWindow(child)
        child.setWindowState(QtCore.Qt.WindowMaximized)

        self.showMaximized()


    def showSettingsDialog(self):
        d = QDialog()
        # b1 = QPushButton("ok", d)
        # b1.move(50, 50)
        d.setWindowTitle("CQCad Settings")
        # d.setWindowModality(Qt.ApplicationModal)
        d.exec_()

        # TODO: Init with keybindings, execute_on_save, use_external_editor, max_line_length settings, line_numbers, cad_engine


def main():
    app = QApplication(sys.argv)
    cqcad = CQCADGui()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()