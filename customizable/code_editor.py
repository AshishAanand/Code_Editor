from PyQt5 import QtCore, QtGui, QtWidgets
from syntax_highlighter import PythonHighlighter, JavaScriptHighlighter
from pygments.lexers import get_lexer_by_name
import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QPlainTextEdit, QTextEdit, QCompleter, QListView, QAbstractItemView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, Qt, QStringListModel


class LineNumberArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QtCore.QSize(self.code_editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.code_editor.lineNumberAreaPaintEvent(event)


class CodeEditor(QtWidgets.QPlainTextEdit):

    text_changed = pyqtSignal(str)
    selection_made = pyqtSignal(str)  # For selected autocomplete suggestion

    def __init__(self, language="Python", parent=None):
        super().__init__(parent)
        self.language = language
        self.highlighter = None
        self.setLanguage(language)
        self.line_number_area = LineNumberArea(self)
        self.setFont(QFont("Fira Code", 12))
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #282c34;
                color: #abb2bf;
                border: 1px solid #3e4451;
                border-radius: 6px;
                padding: 8px;
            }
            QPlainTextEdit:focus {
                border: 1px solid #61afef;
            }
        """)

        # Adding line number area
        self.line_number_area = LineNumberArea(self)
        self.setViewportMargins(40, 0, 0, 0)  # Leave space for the line numbers

        # Signals from the document
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.handleCursorChange)
        self.updateLineNumberAreaWidth(0)

        

        self.setFont(QFont("Courier New", 12))

        self.setStyleSheet("background-color: #fff; color: #34495e;")  # Light theme for the editor
        self.setTabChangesFocus(True)
        self.file_path = None  # To keep track of the current file path


        self.textChanged.connect(self.emit_text_change)

        # Autocomplete Dropdown
        
        self.autocomplete = AutocompleteDropdown(self)
        self.autocomplete.activated.connect(self.insert_autocomplete_suggestion)
        self.autocomplete.popup().setStyleSheet("""
                QListView {
                    background-color: #282c34;
                    color: #dcdcdc;
                    border: 1px solid #3e4451;
                    padding: 5px;
                }
                QListView::item {
                    padding: 5px;
                    border-radius: 4px;
                }
                QListView::item:hover {
                    background-color: #3e4451;
                    color: #ffffff;
                }
                QListView::item:selected {
                    background-color: #61afef;
                    color: #ffffff;
                }
            """)

    
    def emit_text_change(self):
        """Emit the text_changed signal with the current editor content."""
        text = self.toPlainText()
        self.text_changed.emit(text)

    def insert_autocomplete_suggestion(self, text):
        """Insert the selected suggestion into the editor."""
        cursor = self.textCursor()
        cursor.select(cursor.WordUnderCursor)
        cursor.insertText(text)
        self.setTextCursor(cursor)

    def keyPressEvent(self, event):
        """Show autocomplete dropdown on key events."""
        super().keyPressEvent(event)
        if event.key() in (Qt.Key_Space, Qt.Key_Tab):
            self.autocomplete.complete()
    
    def setLanguage(self, language):
        """Switch syntax highlighting based on the selected language."""
        self.language = language
        if self.highlighter:
            self.highlighter.setDocument(None)  # Disconnect the previous highlighter
        if language == "Python":
            self.highlighter = PythonHighlighter(self.document())
        elif language == "JavaScript":
            self.highlighter = JavaScriptHighlighter(self.document())
        else:
            print(f"Warning: Language '{language}' not recognized. No syntax highlighting applied.")
            self.highlighter.setDocument(self.document())  # Connect the new highlighter

    def openFile(self, file_path):
        """Open a file and load its contents into the editor."""
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.setPlainText(content)
                self.file_path = file_path
        except FileNotFoundError:
            self.showError("File Not Found", f"The file '{file_path}' does not exist.")
        except Exception as e:
            self.showError("Error opening file", str(e))

    def saveFile(self):
        """Save the current content of the editor to the current file."""
        if self.file_path:
            try:
                with open(self.file_path, 'w') as file:
                    file.write(self.toPlainText())
            except Exception as e:
                self.showError("Error saving file", str(e))
        else:
            self.saveFileAs()

    def saveFileAs(self):
        """Save the current content of the editor to a new file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "All Files (*)")
        if file_path:
            self.file_path = file_path
            self.saveFile()

    def newFile(self, file_path):
        """Create a new file and clear the editor."""
        try:
            with open(file_path, 'w') as file:
                file.write('')
            self.setPlainText('')
            self.file_path = file_path
        except Exception as e:
            self.showError("Error creating new file", str(e))

    def newFolder(self, folder_name):
        """Create a new folder."""
        try:
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                self.showMessage("Folder Created", f"Folder '{folder_name}' created successfully.")
            else:
                self.showMessage("Folder Exists", f"Folder '{folder_name}' already exists.")
        except Exception as e:
            self.showError("Error creating folder", str(e))

    def deleteFile(self):
        """Delete the current file."""
        if self.file_path and os.path.exists(self.file_path):
            try:
                os.remove(self.file_path)
                self.setPlainText('')
                self.file_path = None
                self.showMessage("File Deleted", f"File '{self.file_path}' deleted successfully.")
            except Exception as e:
                self.showError("Error deleting file", str(e))
        else:
            self.showError("File not found", "The file to delete does not exist.")

    def showMessage(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec_()

    def showError(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec_()

    def set_language(self, language):
        self.highlighter.language = language
        self.highlighter.lexer = get_lexer_by_name(language)
        self.highlighter.rehighlight()

    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        space = 2 + self.fontMetrics().horizontalAdvance('5') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QtCore.QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())
        )

    def lineNumberAreaPaintEvent(self, event):
        painter = QtGui.QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QtCore.Qt.gray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        current_block = self.textCursor().block()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QtCore.Qt.white)
                if block == current_block:
                    painter.setPen(QtCore.Qt.red)
                painter.drawText(0, int(top), self.line_number_area.width(), int(self.fontMetrics().height()),
                                 QtCore.Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def handleCursorChange(self):
        self.line_number_area.update()


class AutocompleteDropdown(QCompleter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setFilterMode(Qt.MatchContains)
        self.setModel(QStringListModel())
        self.popup().setViewMode(QListView.ListMode)
        self.popup().setSelectionBehavior(QAbstractItemView.SelectRows)

    def update_suggestions(self, suggestions):
        """Update autocomplete suggestions dynamically."""
        self.model().setStringList(suggestions)
        self.complete()
