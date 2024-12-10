import sys
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QAction, QFileDialog,
    QPlainTextEdit, QMessageBox, QStatusBar, QLabel
)
from PyQt5.QtGui import QIcon
import os
from code_editor import CodeEditor  # Assuming CodeEditor is in code_editor.py
from PyQt5 import QtCore, QtGui, QtWidgets


# class DraggableLabel(QLabel):
#     """A simple draggable QLabel."""
#     def __init__(self, text, parent=None):
#         super().__init__(text, parent)
#         self.setStyleSheet("background-color: #3498db; color: white; padding: 5px; border-radius: 5px;")
#         self.setAlignment(Qt.AlignCenter)
#         self.setFixedSize(100, 30)  # Set the size of the label
        
#         # Set the font size correctly
#         font = self.font()
#         font.setPointSize(10)
#         self.setFont(font)

#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.drag_start_pos = event.pos()

#     def mouseMoveEvent(self, event):
#         if event.buttons() == Qt.LeftButton:
#             drag_distance = (event.pos() - self.drag_start_pos).manhattanLength()
#             if drag_distance > QApplication.startDragDistance():
#                 self.move(self.mapToParent(event.pos() - self.drag_start_pos))



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 820)
        MainWindow.setStyleSheet("background-color: rgb(40, 40, 40);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Set up toolbar with updated icons and professional look
        toolbar = QToolBar("File Operations")
        self.addToolBar(toolbar)
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


    def openFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file_path:
            self.editor.openFile(file_path)
            self.statusBar.showMessage(f"Opened: {file_path}", 2000)

    def saveFile(self):
        if self.editor.file_path:
            self.editor.saveFile()
            self.statusBar.showMessage(f"Saved: {self.editor.file_path}", 2000)
        else:
            self.saveFileAs()

    def saveFileAs(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "All Files (*)")
        if file_path:
            self.editor.file_path = file_path
            self.editor.saveFile()
            self.statusBar.showMessage(f"Saved As: {file_path}", 2000)

    def newFile(self):
        new_file_name, _ = QFileDialog.getSaveFileName(self, "New File", "", "All Files (*)")
        if new_file_name:
            self.editor.newFile(new_file_name)
            self.statusBar.showMessage(f"Created: {new_file_name}", 2000)

    def newFolder(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_name:
            self.editor.newFolder(folder_name)
            self.statusBar.showMessage(f"Folder Created: {folder_name}", 2000)

    def deleteFile(self):
        if self.editor.file_path:
            self.editor.deleteFile()
            self.statusBar.showMessage(f"Deleted: {self.editor.file_path}", 2000)
        else:
            self.showMessage("Error", "No file to delete.")

    def showMessage(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
