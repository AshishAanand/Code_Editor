from PyQt5 import QtCore, QtGui, QtWidgets
from syntax_highlighter import SyntaxHighlighter
from PyQt5.QtGui import QTextDocument, QIcon
from pygments.lexers import get_lexer_by_name  # Import this
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QAction, QFileDialog,
    QPlainTextEdit, QMessageBox, QStatusBar, QLabel
)
from PyQt5.QtCore import Qt, QSize, QPoint
import sys


class LineNumberArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QtCore.QSize(self.code_editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.code_editor.lineNumberAreaPaintEvent(event)


class CodeEditor(QtWidgets.QPlainTextEdit):  # Using QPlainTextEdit
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)

        # Signals from the document
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)  # Signal provides rect and dy
        self.cursorPositionChanged.connect(self.handleCursorChange)
        self.updateLineNumberAreaWidth(0)
    
        self.highlighter = SyntaxHighlighter(self.document(), language="python")

    def set_language(self, language):
        self.highlighter.language = language
        self.highlighter.lexer = get_lexer_by_name(language)
        self.highlighter.rehighlight()


    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('15') * digits
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
        painter.fillRect(event.rect(), QtCore.Qt.darkGray)

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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 820)
        MainWindow.setStyleSheet("background-color: rgb(40, 40, 40);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Set up toolbar with updated icons and professional look
        self.toolbar = self.addToolBar("File Operations")
        self.toolbar.setIconSize(QSize(24, 24))  # Increase icon size for visibility
        self.toolbar.setStyleSheet("background-color: #2c3e50; color: white;")  # Dark toolbar

        # Add actions to toolbar
        open_action = QAction(QIcon("icons/open.png"), "Open File", self)
        open_action.triggered.connect(self.openFile)
        self.toolbar.addAction(open_action)

        save_action = QAction(QIcon("icons/save.png"), "Save File", self)
        save_action.triggered.connect(self.saveFile)
        self.toolbar.addAction(save_action)

        new_file_action = QAction(QIcon("icons/new-file.png"), "New File", self)
        new_file_action.triggered.connect(self.newFile)
        self.toolbar.addAction(new_file_action)

        new_folder_action = QAction(QIcon("icons/new-folder.png"), "New Folder", self)
        new_folder_action.triggered.connect(self.newFolder)
        self.toolbar.addAction(new_folder_action)

        delete_action = QAction(QIcon("icons/delete.png"), "Delete File", self)
        delete_action.triggered.connect(self.deleteFile)
        self.toolbar.addAction(delete_action)

        # File Manager Panel
        self.file_manager = QtWidgets.QLabel(self.centralwidget)
        self.file_manager.setGeometry(QtCore.QRect(60, 0, 200, 871))
        self.file_manager.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.file_manager.setObjectName("file_manager")

        # Side bar


        # File Names Label
        self.file_names = QtWidgets.QLabel(self.centralwidget)
        self.file_names.setGeometry(QtCore.QRect(60, 20, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.file_names.setFont(font)
        self.file_names.setStyleSheet(
            "background-color: rgb(30, 30, 30); color: white; padding: 5px; border-radius: 5px;"
        )
        self.file_names.setAlignment(QtCore.Qt.AlignCenter)
        self.file_names.setObjectName("file_names")

        # Workspace
        self.workspace_width = 1090
        self.workspace_height = 665
        self.workspace = CodeEditor(self.centralwidget)
        self.workspace.setGeometry(QtCore.QRect(260, 0, self.workspace_width, self.workspace_height))
        self.workspace.setStyleSheet(
            "background-color: rgb(20, 20, 20); padding: 20px; color: white; font-size: 16px; font-family: Consolas;"
        )
        self.workspace.setObjectName("workspace")

        # Status Bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setStyleSheet("background-color: rgb(60, 60, 60); color: white;")
        MainWindow.setStatusBar(self.statusbar)

        # Menu Bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.menubar.setFont(font)
        self.menubar.setStyleSheet("background-color: rgb(70, 70, 70); color: white;")
        self.menubar.setObjectName("menubar")

        # Creating File Tab
        # self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile = self.menubar.addMenu("File")
        self.menuFile.setStyleSheet("color: white;")
        self.menuFile.setObjectName("menuFile")

        # Adding actions to File tab
        self.new_file = self.menuFile.addAction("New")
        # self.new_file.triggered.connect(self.new_file_action)
        self.new_file.setShortcut("Ctrl+N")

        self.open_file = self.menuFile.addAction("Open")
        self.open_file.setShortcut("Ctrl+O")
        # self.open_file.trigger.connect(self.open_file_action)

        self.open_folder = self.menuFile.addAction("Open Folder")
        self.open_folder.setShortcut("Ctrl+Shift+O")
        

        self.save_file = self.menuFile.addAction("Save")
        self.save_file.setShortcut("Ctrl+S")

        # Creating Edit Tab
        # self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit = self.menubar.addMenu("Edit")
        self.menuEdit.setStyleSheet("color: white;")
        self.menuEdit.setObjectName("menuEdit")

        # Adding actions to Edit tab
        self.undo = self.menuEdit.addAction("Undo")
        # self.undo.triggered.connect(self.undo_action)
        self.undo.setShortcut("Ctrl+Z")

        self.redo = self.menuEdit.addAction("Redo")
        # self.redo.triggered.connect(self.redo_action)
        self.redo.setShortcut("Ctrl+Y")

        self.cut = self.menuEdit.addAction("Cut")
        # self.cut.triggered.connect(self.cut_action)
        self.cut.setShortcut("Ctrl+X")

        self.copy = self.menuEdit.addAction("Copy")
        # self.copy.triggered.connect(self.copy_action)
        self.copy.setShortcut("Ctrl+C")

        self.past = self.menuEdit.addAction("Past")
        # self.past.triggered.connect(self.past_action)
        self.past.setShortcut("Ctrl+V")

        self.run_code = self.menubar.addMenu("Run")
        self.run_code.setStyleSheet("color: white;")
        self.run_code.setObjectName("run_code")

        # Adding actions to Run tab
        self.run_this_file = self.run_code.addAction("Run Code")
        self.run_this_file.triggered.connect(self.run_this_file_action)
        self.run_this_file.setShortcut("Ctrl+R")



        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.run_code.menuAction())

        # Retranslate UI
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    # def set_up_body(self):

    #     # Body

    #     body_frame = QFarme()
    #     body_frame.setFrameShape(QFrame.NoFrame)
    #     body_frame = setFrameShadow(QFrame.Plain)
    #     body_frame.setLineWidth(0)
    #     body_frame.setMidLineWidth(0)
    #     body_frame.setContentMargins(0,0,0,0)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Code Editor"))
        self.file_names.setText(_translate("MainWindow", "File Manager"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.run_code.setTitle(_translate("MainWindow", "Run"))

    def run_this_file_action(self):
        print("Run this file action")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
