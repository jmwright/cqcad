import sys
import os
import uuid
from _version import __version__
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, qApp, QMessageBox, QMenu, QDialog, QLabel, QDockWidget, QMdiArea, QSizePolicy, QToolButton, QMdiSubWindow
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSettings
from components.CodeEditor import CodeEditor
from components.DockWidget import DockWidget
from components.SettingsDialog import SettingsDialog
from components.NewDialog import NewDialog
from components.Viewer3D import Viewer3D
from OCC.Display.backend import load_backend, get_qt_modules


class CQCadWindow(QMainWindow):
    # Platform independent application settings
    settings = QSettings('cqcad', 'settings')
    guiState = QSettings('cqcad', 'gui')
    menuList = []

    def __init__(self):
        super(CQCadWindow, self).__init__()

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

    def clickHelp(self):
        """
        Displays a dialog with information about where to find help.

        :return: None
        """
        docLabel = QLabel("http://dcowden.github.io/cadquery/")
        docLabel.setOpenExternalLinks = True

        varTitle = QtCore.QCoreApplication.translate('cqcad', "Finding Help")
        varMsg = QtCore.QCoreApplication.translate('cqcad',
                                                   "CQCad 2D/3D CAD\r\nVersion: " + __version__ + "\r\n\r\nDocumentation: http://dcowden.github.io/cadquery/\r\nVideo Tutorials: https://www.youtube.com/playlist?list=PLMXw3KF1-YfUeFnw6Ich9jvgYjyjiBS3w\r\nUser Group: https://groups.google.com/forum/#!forum/cadquery")

        msgBox = QMessageBox.about(self, varTitle, varMsg)
        # msgBox.setTextFormat(Qt.RichText)


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

            # Keep track of the state of the GUI for the user
            self.guiState.setValue('mouse_first_enabled', True)
            self.guiState.setValue('script_first_enabled', False)

        elif sending_button.objectName() == 'script_first':
            self.mouse1stAct.setChecked(False)

            # Keep track of the state of the GUI for the user
            self.guiState.setValue('mouse_first_enabled', False)
            self.guiState.setValue('script_first_enabled', True)


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

    def getLayouts(self):
        """
        Finds a list of all the layouts that are installed.
        :return: The titles of all the layouts that are installed.
        """
        module_base_path = os.path.dirname(__file__)
        layouts_path = os.path.join(module_base_path, 'layouts')

        titles = []
        functions = {}

        for module in os.listdir(layouts_path):
            if module.endswith('.py') and module != "__init__.py":
                baseName = os.path.splitext(module)[0]
                name = "layouts." + baseName
                mod = __import__(name, fromlist=[baseName])

                titles.append(mod.__title__)
                functions[mod.__title__.replace(' ', '_').lower()] = mod.execute

        return (titles, functions)

    def loadExtensions(self):
        """
        Finds all of the extensions that are installed and instantiates them.
        :return: None
        """
        module_base_path = os.path.dirname(__file__)
        layouts_path = os.path.join(module_base_path, 'extensions')

        # Load all the extensions and for now tell them to run their setup function to make changes to the GUI
        for module in os.listdir(layouts_path):
            if module.endswith('.py') and module != "__init__.py":
                baseName = os.path.splitext(module)[0]
                name = "extensions." + baseName
                mod = __import__(name, fromlist=[baseName])

                enabled = self.guiState.value(name + "_checked", type=bool)

                # Only load the controls for the extension if it is selected
                if enabled:
                    mod.setup(self)

                act = QAction('&' + baseName, self, checkable=True)
                # act.setShortcut('F6')
                act.setStatusTip(baseName)
                act.setChecked(enabled)
                act.setObjectName(baseName)
                act.triggered.connect(self.toggleExtension)
                self.extsMenu.addAction(act)

                self.menuList.append(act)

    def fireFunction(self):
        """
        Allows us to fire dynamically loaded functions while avoiding a mess
        with a collections.namedtuple import error.
        :return: None
        """
        widget = self.sender().objectName()

        # Avoid an exception from the key not being present
        if widget in self.funcs.keys():
            self.funcs[widget](self.mdiArea)

    def toggleExtsMenuVisibility(self):
        """
        Allows the user to click on the extensions toolbutton and still get the
        drop-down menu.
        :return: None
        """
        if not self.extsMenu.isVisible():
            self.extsButton.showMenu()

    def toggleExtension(self):
        baseName = self.sender().objectName()
        name = "extensions." + baseName
        mod = __import__(name, fromlist=[baseName])

        if self.sender().isChecked():
            mod.setup(self)
            self.guiState.setValue(name + "_checked", True)
        else:
            mod.tearDown(self)
            self.guiState.setValue(name + "_checked", False)

        self.guiState.sync()

    def showSettingsDialog(self):
        self.settingsDlg = SettingsDialog(self)

        # TODO: Init with keybindings, execute_on_save, use_external_editor, max_line_length settings, line_numbers, cad_engine

    def showNewDialog(self):
        newDlg = NewDialog(self)

    def addScriptWindow(self):
        """
        Opens a template in the Python script editor
        :return: None
        """
        subWin = QMdiSubWindow()
        child = CodeEditor(self)
        subWin.setWidget(child)
        child.setObjectName('script:' + str(uuid.uuid1()))
        self.mdiArea.setWindowIcon(QIcon('content/images/python_logo.svg'))
        self.mdiArea.addSubWindow(subWin)
        subWin.setWindowState(QtCore.Qt.WindowMaximized)
        subWin.setWindowTitle('untitled.py')

        file = open("templates/script_template.py", "r")
        templateText = file.read()

        child.setPlainText(templateText)

    def addPartWindow(self):
        """
        For now, default to opening a part template in the Python script editor
        :return: None
        """
        subWin = QMdiSubWindow()
        self.mdiArea.setWindowIcon(QIcon('content/images/python_logo.svg'))
        self.mdiArea.addSubWindow(subWin)

        # backend_str = "qt-pyqt5"
        # used_backend = load_backend(backend_str)
        # from OCC.Display.qtDisplay import qtViewer3d

        # Set the part window up differently based on whether the user has
        # selected the mouse first or script first mode
        if self.mouse1stAct.isChecked():
            child = Viewer3D(self)
            subWin.setWidget(child)

            # If we don't do this the window title bar can disappear
            subWin.setMinimumSize(100, 300)

            subWin.setWindowState(QtCore.Qt.WindowMaximized)

            # For now display a default object
            child.InitDriver()
            child._display.Test()
        else:
            child = CodeEditor(self)
            subWin.setWidget(child)

            file = open("templates/part_template.py", "r")
            templateText = file.read()

            child.setPlainText(templateText)

            subWin.setWindowState(QtCore.Qt.WindowMaximized)

    def addAsmWindow(self):
        """
        For now, default to opening a part template in the Python script editor
        :return: None
        """
        # For now, default to opening a script editor
        child = CodeEditor(self)
        self.mdiArea.setWindowIcon(QIcon('content/images/python_logo.svg'))
        self.mdiArea.addSubWindow(child)
        child.setWindowState(QtCore.Qt.WindowMaximized)

        file = open("templates/assembly_template.py", "r")
        templateText = file.read()

        child.setPlainText(templateText)

    def executeScript(self):
        """
        Executes the script in the active editor window and displays it.
        """
        # Get the active window so we can get the script and match the title
        activeWin = self.mdiArea.activeSubWindow()
        scriptTitle = activeWin.windowTitle()

        # If this isn't a script window we need to handle it differently
        if ".py" not in scriptTitle:
            self.statusBar().showMessage('Cannot Execute From a Non-Script Window')
            return

        # See if the 3D view is somewhere in the MDI subwindows
        subWin = self.getSubwindowByName(scriptTitle + " (3D)")

        # If the 3D view doesn't exist, create it
        if subWin == None:
            # Set up a new 3D view window
            subWin = QMdiSubWindow()
            # self.mdiArea.setWindowIcon(QIcon('content/images/python_logo.svg'))
            self.mdiArea.addSubWindow(subWin)

            child = Viewer3D(self)
            subWin.setWidget(child)
            subWin.setWindowTitle(scriptTitle + " (3D)")

            # If we don't do this the window title bar can disappear
            subWin.setMinimumSize(100, 300)

            subWin.setWindowState(QtCore.Qt.WindowMaximized)

            # For now display a default object
            child.InitDriver()
            child._display.Test()

        # Extract the text from the script window, execute it, and display the result
        scriptText = activeWin.widget().toPlainText()
        print(scriptText)

    def getSubwindowByName(self, name):
        """
        Searches for a subwindow in the MDI area by name
        """
        foundWin = None
        for subwin in self.mdiArea.subWindowList():
            if subwin.windowTitle() == name:
                foundWin = subwin

        return foundWin

    def setInitialGUIState(self):
        # Mouse vs script mode
        self.guiState.setValue('script_first_enabled', True)
        self.guiState.setValue('mouse_first_enabled', False)

        # Widget visibility
        self.guiState.setValue('dock_visible', True)

        # Make sure we only enter this code once
        self.guiState.setValue('first_run_over', True)

    def initUI(self):
        # Handle setting things up if this is the first time this app has been run
        if not self.guiState.value('first_run_over', type=bool):
            self.setInitialGUIState()

        # Translations of menu items
        exitName = QtCore.QCoreApplication.translate('cqcad', "Exit")
        exitTip = QtCore.QCoreApplication.translate('cqcad', "Exit application")
        newName = QtCore.QCoreApplication.translate('cqcad', "New")
        newTip = QtCore.QCoreApplication.translate('cqcad', "New")
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
        layoutsName = QtCore.QCoreApplication.translate('cqcad', "Layouts")
        layoutsTip = QtCore.QCoreApplication.translate('cqcad', "Layouts")
        setsName = QtCore.QCoreApplication.translate('cqcad', "Settings")
        setsTip = QtCore.QCoreApplication.translate('cqcad', "Settings")
        fileName = QtCore.QCoreApplication.translate('cqcad', "File")
        rcntName = QtCore.QCoreApplication.translate('cqcad', "Recent")
        exName = QtCore.QCoreApplication.translate('cqcad', "Examples")
        editName = QtCore.QCoreApplication.translate('cqcad', "Edit")
        viewName = QtCore.QCoreApplication.translate('cqcad', "View")
        modesName = QtCore.QCoreApplication.translate('cqcad', "Modes")
        panelsName = QtCore.QCoreApplication.translate('cqcad', "Panels")
        layoutMenuName = QtCore.QCoreApplication.translate('cqcad', "Layout")
        layoutMenuTip = QtCore.QCoreApplication.translate('cqcad', "Layout")
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
        docsName = QtCore.QCoreApplication.translate('cqcad', "Documentation")
        docsTip = QtCore.QCoreApplication.translate('cqcad', "Documentation")
        vidsName = QtCore.QCoreApplication.translate('cqcad', "Video Tutorials")
        vidsTip = QtCore.QCoreApplication.translate('cqcad', "Video Tutorials")
        uGroupName = QtCore.QCoreApplication.translate('cqcad', "User Group")
        uGroupTip = QtCore.QCoreApplication.translate('cqcad', "User Group")
        extsToolName = QtCore.QCoreApplication.translate('cqcad', "Extensions")
        extsToolTip = QtCore.QCoreApplication.translate('cqcad', "Extensions")

        #self.setGeometry(300, 300, 250, 150)

        # The central MDI window area
        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        self.setWindowTitle('CQCad')
        self.setWindowIcon(QtGui.QIcon('content/images/cadquery_logo_dark.svg'))
        self.statusBar().showMessage('Ready')

        # Set up our menu
        exitAct = QAction(QIcon('content/images/Material/ic_exit_to_app_24px.svg'), '&' + exitName, self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip(exitTip)
        exitAct.triggered.connect(qApp.quit)

        newAct = QAction('&' + newName, self)
        newAct.setShortcut('Ctrl+N')
        newAct.setStatusTip(newTip)
        newAct.triggered.connect(self.showNewDialog)

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

        self.mouse1stAct = QAction('&' + m1stName, self, checkable=True)
        # self.mouse1stAct.setShortcut('F6')
        self.mouse1stAct.setStatusTip(m1stTip)
        self.mouse1stAct.setChecked(self.guiState.value('mouse_first_enabled', type=bool))
        self.mouse1stAct.setObjectName('mouse_first')
        self.mouse1stAct.triggered.connect(self.switchModes)

        self.script1stAct = QAction('&' + s1stName, self, checkable=True)
        # self.script1stAct.setShortcut('F6')
        self.script1stAct.setStatusTip(s1stTip)
        self.script1stAct.setChecked(self.guiState.value('script_first_enabled', type=bool))
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

        self.dockAct = QAction('&' + dockName, self, checkable=True)
        self.dockAct.setStatusTip(dockName)
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

        layoutsAct = QAction('&' + layoutsName, self)
        # layoutsAct.setShortcut('F6')
        layoutsAct.setStatusTip(layoutsTip)
        layoutsAct.triggered.connect(self.notImplemented)

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

        docsAct = QAction('&' + docsName, self)
        # docsAct.setShortcut('F1')
        docsAct.setStatusTip(docsTip)
        docsAct.triggered.connect(self.notImplemented)

        vidsAct = QAction('&' + vidsName, self)
        # vidsAct.setShortcut('F1')
        vidsAct.setStatusTip(vidsTip)
        vidsAct.triggered.connect(self.notImplemented)

        uGroupAct = QAction('&' + uGroupName, self)
        # uGroupAct.setShortcut('F1')
        uGroupAct.setStatusTip(uGroupTip)
        uGroupAct.triggered.connect(self.notImplemented)

        aboutAct = QAction(QIcon('content/images/Material/ic_help_24px.svg'), '&' + abtName, self)
        aboutAct.setShortcut('F1')
        aboutAct.setStatusTip(abtTip)
        aboutAct.triggered.connect(self.clickAbout)

        self.helpAct = QAction(QIcon('content/images/Material/ic_help_24px.svg'), '&' + abtName, self)
        # self.helpAct.setShortcut('F1')
        self.helpAct.setStatusTip(abtTip)
        self.helpAct.triggered.connect(self.clickHelp)

        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&' + fileName)
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
        editMenu = self.menubar.addMenu('&' + editName)
        editMenu.addAction(libsAct)
        editMenu.addAction(extsAct)
        editMenu.addAction(layoutsAct)
        editMenu.addAction(settingsAct)
        viewMenu = self.menubar.addMenu('&' + viewName)
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
        self.layoutMenu = QMenu(layoutMenuName)
        viewMenu.addMenu(self.layoutMenu)
        # projMenu = menubar.addMenu('&Project')
        self.helpMenu = self.menubar.addMenu('&' + helpName)
        self.helpMenu.addAction(docsAct)
        self.helpMenu.addAction(vidsAct)
        self.helpMenu.addAction(uGroupAct)
        self.helpMenu.addAction(aboutAct)

        # Load layouts dynamically
        (layouts, self.funcs) = self.getLayouts()
        for layout in layouts:
            act = QAction('&' + layout, self)
            act.setStatusTip(layout)
            act.setObjectName(layout.replace(' ', '_').lower())
            act.triggered.connect(self.fireFunction)

            self.layoutMenu.addAction(act)

        # The CadQuery logo
        # logoLabel = QLabel()
        # logoLabel.setPixmap(QPixmap('content/images/cadquery_logo_dark.svg'))

        # Toolbar for CAD controls and extension controls
        self.toolbar = self.addToolBar('Main Tools')
        # self.toolbar.addWidget(logoLabel)
        self.toolbar.addAction(frontViewAct)
        self.toolbar.addAction(backViewAct)
        self.toolbar.addAction(topViewAct)
        self.toolbar.addAction(bottomViewAct)
        self.toolbar.addAction(leftViewAct)
        self.toolbar.addAction(rightViewAct)
        self.toolbar.addAction(axioViewAct)
        self.toolbar.addAction(fitAllAct)
        self.toolbar.addSeparator()

        self.toolbar.addAction(self.helpAct)

        # Drop-dowm menu that lets users select which extensions they want active
        self.extsButton = QToolButton(self.toolbar)
        self.extsButton.setIcon(QIcon('content/images/Material/ic_extension_black_24px.svg'))
        self.extsMenu = QMenu(self.extsButton)
        self.extsButton.clicked.connect(self.toggleExtsMenuVisibility)
        self.extsButton.setMenu(self.extsMenu)
        self.extsButton.setPopupMode(QToolButton.MenuButtonPopup)

        # Start up all extensions
        self.loadExtensions()

        # Add the extensions dropdown at the right side of the toolbar
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)
        self.toolbar.addWidget(self.extsButton)

        # Side dock for things like the object viewer
        self.dock = DockWidget(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        self.dock.setMinimumSize(200, 100)
        self.setInitialDockState()

        self.showMaximized()
