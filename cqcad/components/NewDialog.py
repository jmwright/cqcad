from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QToolButton

class NewDialog(QDialog):
    buttonSize = 100
    iconSize = 60

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        # super(NewDialog, self).__init__()

        self.layout = QHBoxLayout(self)

        self.resize(500, 100)

        # New script button
        scriptButton = QToolButton(self)
        scriptButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        scriptButton.setText("Script")
        scriptButton.setIcon(QIcon('content/images/Material/ic_code_black_24px.svg'))
        scriptButton.setIconSize(QSize(self.iconSize, self.iconSize))
        scriptButton.setFixedSize(QSize(self.buttonSize, self.buttonSize))
        scriptButton.clicked.connect(parent.addScriptWindow)
        scriptButton.clicked.connect(self.finish)

        # New part button
        partButton = QToolButton(self)
        partButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        partButton.setText("Part")
        partButton.setIcon(QIcon('content/images/Material/ic_toys_black_24px.svg'))
        partButton.setIconSize(QSize(self.iconSize, self.iconSize))
        partButton.setFixedSize(QSize(self.buttonSize, self.buttonSize))
        partButton.clicked.connect(parent.addPartWindow)
        partButton.clicked.connect(self.finish)

        # New assembly button
        asmButton = QToolButton(self)
        asmButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        asmButton.setText("Assembly")
        asmButton.setIcon(QIcon('content/images/Material/ic_pie_chart_black_24px.svg'))
        asmButton.setIconSize(QSize(self.iconSize, self.iconSize))
        asmButton.setFixedSize(QSize(self.buttonSize, self.buttonSize))
        asmButton.clicked.connect(parent.addAsmWindow)
        asmButton.clicked.connect(self.finish)

        # New project button
        projButton = QToolButton(self)
        projButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        projButton.setText("Project")
        projButton.setIcon(QIcon('content/images/Material/ic_create_new_folder_black_24px.svg'))
        projButton.setIconSize(QSize(self.iconSize, self.iconSize))
        projButton.setFixedSize(QSize(self.buttonSize, self.buttonSize))
        projButton.clicked.connect(parent.notImplemented)

        self.layout.addWidget(scriptButton)
        self.layout.addWidget(partButton)
        self.layout.addWidget(asmButton)
        self.layout.addWidget(projButton)

        self.setWindowTitle("New")
        self.setWindowModality(Qt.ApplicationModal)
        self.exec_()

    def finish(self):
        """
        Clean up and close the dialog
        :return: None
        """
        self.done(0)