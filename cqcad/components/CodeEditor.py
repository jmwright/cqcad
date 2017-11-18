from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QSettings, QRect, pyqtSlot, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QPlainTextEdit, QWidget

class LineNumberArea(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.codeEditor=parent

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(),0)

    def paintEvent(self,event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self, parent):
        # super(CodeEditor, self).__init__()
        QPlainTextEdit.__init__(self, parent)
        self.lineNumberArea = LineNumberArea(self)
        self.setTabStopWidth(20)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)

        self.initUI()

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while (block.isValid() and top <= event.rect().bottom()):
            if (block.isValid and bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(QtCore.Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(),
                                 self.fontMetrics().height(),
                                 QtCore.Qt.AlignCenter, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def lineNumberAreaWidth(self):
        digits = 1
        dMax = max(1, self.blockCount())
        while (dMax >= 10):
            dMax /= 10
            digits += 1
        return 3 + self.fontMetrics().width('9') * digits

    def resizeEvent(self, event):
        QPlainTextEdit.resizeEvent(self, event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(),
                  cr.height()))

    @pyqtSlot(int)
    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    @pyqtSlot(QRect, int)
    def updateLineNumberArea(self, rect, dy):
        if (dy != 0):
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(),
                                       self.lineNumberArea.width(),
                                       rect.height())
        if (rect.contains(self.viewport().rect())):
            self.updateLineNumberAreaWidth(0)

    def initUI(self):
        pass