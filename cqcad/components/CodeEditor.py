from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QSettings, QRect, pyqtSlot, Qt, QRegExp
from PyQt5.QtGui import QPainter, QSyntaxHighlighter, QTextCharFormat, QFont, QColor, QTextCursor
from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit, QWidget

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
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()
        self.highlighter = CHighlighter(self.document())

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

    @pyqtSlot()
    def highlightCurrentLine(self):
        extraSelections = []
        if (not self.isReadOnly()):
            lineColor = QColor("#E0EEEE")
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextCharFormat.FullWidthSelection, True)
            selection.cursor=self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def keyPressEvent(self,event):
        customKey=False
        #AutoTab
        if (event.key()==Qt.Key_Enter or event.key()==16777220):
            customKey=True
            numTab=0
            #new line
            newBlock=self.textCursor().block()
            currLine=newBlock.text()
            tabRE=QRegExp("^[\t]*")
            tabRE.indexIn(currLine)
            numTab=tabRE.matchedLength()
            if (currLine.strip()[-1] == "{"):
                numTab += 1
            QPlainTextEdit.keyPressEvent(self,event)
            if (numTab > 0):
                tCursor=self.textCursor()
                for _ in range(0,numTab):
                    tCursor.insertText("\t")

                #automatic close brace
                if currLine.strip()[-1] == "{":
                    tCursor.insertText("\n")
                    for _ in range(0,numTab-1):
                        tCursor.insertText("\t")
                    tCursor.insertText("}")
                    tCursor.movePosition(QTextCursor.PreviousBlock)
                    tCursor.movePosition(QTextCursor.EndOfLine)
                    self.setTextCursor(tCursor)

        if event.key() == Qt.Key_Tab and self.textCursor().hasSelection():
            customKey = True
            selStart=self.textCursor().selectionStart()
            selEnd=self.textCursor().selectionEnd()
            cur=self.textCursor()
            endBlock=self.document().findBlock(selEnd)
            currBlock=self.document().findBlock(selStart)
            while currBlock.position()<=endBlock.position():
                cur.setPosition(currBlock.position())
                cur.insertText("\t")
                currBlock=currBlock.next()

        if event.key() == Qt.Key_Backtab and self.textCursor().hasSelection():
            customKey = True
            selStart=self.textCursor().selectionStart()
            selEnd=self.textCursor().selectionEnd()
            cur=self.textCursor()
            endBlock=self.document().findBlock(selEnd)
            currBlock=self.document().findBlock(selStart)
            while currBlock.position() <= endBlock.position():
                cur.setPosition(currBlock.position())
                if currBlock.text().left(1) == "\t":
                    cur.deleteChar()
                currBlock=currBlock.next()
        if not customKey:
            QPlainTextEdit.keyPressEvent(self, event)

    def initUI(self):
        pass

class CHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        QSyntaxHighlighter.__init__(self, parent)
        self.rules=[]
        self.keywordFormat=QTextCharFormat()
        self.singleLineCommentFormat=QTextCharFormat()
        self.multiLineCommentFormat=QTextCharFormat()
        self.quotaFormat=QTextCharFormat()
        self.functionFormat=QTextCharFormat()
        self.precompilerFormat=QTextCharFormat()
        self.numberFormat=QTextCharFormat()

        self.keywordFormat.setForeground(Qt.darkBlue)
        self.keywordFormat.setFontWeight(QFont.Bold)

        keywords=[]
        keywords.append("\\bclass\\b")
        keywords.append("\\bdef\\b")
        keywords.append("\\bdouble\\b")
        keywords.append("\\benum\\b")
        keywords.append("\\bexplicit\\b")
        keywords.append("\\bfriend\\b")
        keywords.append("\\binline\\b")
        keywords.append("\\bint\\b")
        keywords.append("\\blong\\b")
        keywords.append("\\bnamespace\\b")
        keywords.append("\\boperator\\b")
        keywords.append("\\bprivate\\b")
        keywords.append("\\bprotected\\b")
        keywords.append("\\bpublic\\b")
        keywords.append("\\bshort\\b")
        keywords.append("\\bsignals\\b")
        keywords.append("\\bsigned\\b")
        keywords.append("\\bslots\\b")
        keywords.append("\\bstatic\\b")
        keywords.append("\\bstruct\\b")
        keywords.append("\\btemplate\\b")
        keywords.append("\\btypedef\\b")
        keywords.append("\\btypedef\\b")
        keywords.append("\\btypename\\b")
        keywords.append("\\bunion\\b")
        keywords.append("\\bunsigned\\b")
        keywords.append("\\bvirtual\\b")
        keywords.append("\\bvoid\\b")
        keywords.append("\\breturn\\b")
        keywords.append("\\bvolatile\\b")
        for kw in keywords:
            self.rules.append((QRegExp(kw), self.keywordFormat))

        self.numberFormat.setForeground(Qt.darkRed)
        self.rules.append((QRegExp("\\d+"), self.numberFormat))

        self.quotaFormat.setForeground(Qt.darkGreen)
        self.rules.append((QRegExp("\".*\"") ,self.quotaFormat))

        self.functionFormat.setFontItalic(True)
        self.functionFormat.setForeground(Qt.blue)
        self.rules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"), self.functionFormat))

        self.singleLineCommentFormat.setForeground(Qt.red)
        self.rules.append((QRegExp("//[^\n]*"), self.singleLineCommentFormat))
        self.commentStartExpression = QRegExp("/\\*")
        self.commentEndExpression = QRegExp("\\*/")

        self.multiLineCommentFormat.setForeground(Qt.lightGray)

        self.precompilerFormat.setForeground(Qt.darkCyan)
        self.rules.append((QRegExp("^[ |\t]*#.*"), self.precompilerFormat))

    def highlightBlock(self,text):
        for rule in self.rules:
            re=rule[0]
            index=re.indexIn(text)
            while (index >=0):
                length=re.matchedLength()
                self.setFormat(index,length,rule[1])
                index=re.indexIn(text,index+length)
        self.setCurrentBlockState(0)

        startIndex=0
        if (self.previousBlockState()!=1):
            startIndex=self.commentStartExpression.indexIn(text)
        while (startIndex >=0 ):
            endIndex=self.commentEndExpression.indexIn(text,startIndex)
            if (endIndex==-1):
                self.setCurrentBlockState(1)
                commentLength=text.length()-startIndex
            else:
                commentLength=endIndex-startIndex+self.commentEndExpression.matchedLength()
            self.setFormat(startIndex, commentLength, self.multiLineCommentFormat)
            startIndex=self.commentStartExpression.indexIn(text,startIndex+commentLength)
