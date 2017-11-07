from PyQt5.QtWidgets import QTextEdit

class CodeEdit(QTextEdit):
    def __init__(self):
        super(CodeEdit, self).__init__()

        self.initUI()

    def initUI(self):
        pass