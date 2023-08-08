from PySide2.QtWidgets import QApplication, QMainWindow, QTextEdit, QPlainTextEdit, QVBoxLayout, QWidget
from PySide2.QtGui import QTextCursor, QColor, QTextFormat, QPainter, QFont, QFontMetrics, QWheelEvent
from PySide2.QtCore import QRect, QSize, Qt
from SyntaxHighlighter import *

# Rest of the code remains unchanged

class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super(CodeEditor, self).__init__(parent)
        
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        font = QFont("Consolas", 10)
        font.setStyleHint(QFont.Monospace)
        # Set a monospaced font for the CodeEditor widget
        font.setStyleStrategy(QFont.PreferAntialias)  # Enable anti-aliasing
        self.setFont(font)

        # Calculate the width of four spaces in the current font
        metrics = QFontMetrics(font)
        space_width = metrics.width(" " * 4)
        
        # Set the tab stop width to match the width of four spaces
        self.setTabStopWidth(space_width)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

        # Set the line wrap mode to NoWrap
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        #self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)  # Set tab spacing to four spaces

        self.highlighter = PythonSyntaxHighlighter(self.document())  # Attach the syntax highlighter to the document
        
        # Initialize font size
        self.base_font_size = 14

    def wheelEvent(self, event):
        # Check if Ctrl key is pressed
        if event.modifiers() == Qt.ControlModifier:
            # Get the wheel event delta
            delta = event.angleDelta().y()
            # Increase or decrease the font size based on the delta
            if delta > 0:
                self.base_font_size += 1
            else:
                self.base_font_size -= 1

            # Limit font size to a reasonable range
            self.base_font_size = max(4, min(30, self.base_font_size))

            # Set the new font size
            font = self.font()
            font.setPointSize(self.base_font_size)
            self.setFont(font)
        else:
            # Call the default wheelEvent for other cases
            super(CodeEditor, self).wheelEvent(event)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab and not event.modifiers() & Qt.ShiftModifier:
            # Handle Tab key press
            self.handleTabKeyPress()
        else:
            super(CodeEditor, self).keyPressEvent(event)

    def handleTabKeyPress(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            # Indent all selected lines by four spaces
            selected_blocks = self.get_selected_blocks()
            for block in selected_blocks:
                cursor.setPosition(block.position())
                cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
                cursor.insertText(' ' * 4)
        else:
            # Insert four spaces at the cursor position
            cursor.insertText(' ' * 4)

    def get_selected_blocks(self):
        cursor = self.textCursor()
        start_block = cursor.block()
        end_block = cursor.block()
        if cursor.hasSelection():
            start_block = self.document().findBlock(cursor.selectionStart())
            end_block = self.document().findBlock(cursor.selectionEnd())
            if end_block.position() == cursor.selectionEnd():
                end_block = end_block.previous()
        return range(start_block.blockNumber(), end_block.blockNumber() + 1)
    
    def load_file(self, file_path):
        with open(file_path, 'r') as file:
            self.setPlainText(file.read())

    def update_text(self, file_content):
        self.setPlainText(file_content)

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        
        while max_value >= 10:
            max_value /= 10
            digits += 1
        
        space = 10 + self.fontMetrics().width('9') * digits
        return space
    
    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
    
    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)
    
    def resizeEvent(self, event):
        super(CodeEditor, self).resizeEvent(event)
        
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))
    
    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(35, 35, 35))  # Set the background color to match your dark design
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        # Iterate over visible blocks and draw the line numbers
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.lightGray)
                painter.drawText(0, top, self.lineNumberArea.width(), self.fontMetrics().height(),
                                    Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def highlightCurrentLine(self):
        extra_selections = []
        
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            
            line_color = QColor(Qt.gray).darker(160)
            selection.format.setBackground(line_color)
            
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            
            extra_selections.append(selection)
        
        self.setExtraSelections(extra_selections)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super(LineNumberArea, self).__init__(editor)
        self.codeEditor = editor
    
    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)
    
    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)