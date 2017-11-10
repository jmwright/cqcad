from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

__title__ = QCoreApplication.translate('cqcad', "Scripting")

def setup(mainWindow):
    """
    Modifies the GUI to make this extension usable
    :param mainWindow: The main window of the application so that we can modify what we need
    :return: None
    """
    scriptName = QtCore.QCoreApplication.translate('cqcad', "Scripting")
    execName = QtCore.QCoreApplication.translate('cqcad', "Execute")
    execTip = QtCore.QCoreApplication.translate('cqcad', "Execute script")
    dbgName = QtCore.QCoreApplication.translate('cqcad', "Debug")
    dbgTip = QtCore.QCoreApplication.translate('cqcad', "Debug script")
    validName = QtCore.QCoreApplication.translate('cqcad', "Validate")
    validTip = QtCore.QCoreApplication.translate('cqcad', "Validate script")

    execAct = QAction(QIcon('content/images/Material/ic_play_arrow_24px.svg'), '&' + execName, mainWindow)
    execAct.setShortcut('F2')
    execAct.setStatusTip(execTip)
    execAct.setObjectName('execAct')
    execAct.triggered.connect(mainWindow.notImplemented)

    debugAct = QAction(QIcon('content/images/Material/ic_bug_report_24px.svg'), '&' + dbgName, mainWindow)
    debugAct.setShortcut('F5')
    debugAct.setStatusTip(dbgTip)
    debugAct.setObjectName('debugAct')
    debugAct.triggered.connect(mainWindow.notImplemented)

    validAct = QAction(QIcon('content/images/Material/ic_check_black_24px.svg'), '&' + validName, mainWindow)
    validAct.setShortcut('F6')
    validAct.setStatusTip(validTip)
    validAct.setObjectName('validAct')
    validAct.triggered.connect(mainWindow.notImplemented)

    scriptMenu = mainWindow.menubar.addMenu('&' + scriptName)
    scriptMenu.addAction(execAct)
    scriptMenu.addAction(debugAct)
    scriptMenu.addAction(validAct)
    scriptMenu.setObjectName('scriptMenu')
    mainWindow.menubar.insertMenu(mainWindow.helpMenu.menuAction(), scriptMenu)

    mainWindow.toolbar.addAction(execAct)
    mainWindow.toolbar.addAction(debugAct)
    mainWindow.toolbar.addAction(validAct)

def tearDown(mainWindow):
    """
    Undoes the modifications to the GUI to make it usable for this extension.
    :param mainWindow: The main window of the application so that we can un-modify what we changed before
    :return: None
    """
    execAct = mainWindow.findChild(QAction, "execAct")
    mainWindow.toolbar.removeAction(execAct)
    debugAct = mainWindow.findChild(QAction, "debugAct")
    mainWindow.toolbar.removeAction(debugAct)
    validAct = mainWindow.findChild(QAction, "validAct")
    mainWindow.toolbar.removeAction(validAct)

    menu = mainWindow.findChild(QMenu, "scriptMenu")
    menu.deleteLater()