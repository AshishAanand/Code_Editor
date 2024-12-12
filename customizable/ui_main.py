# import sys
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QTreeView, QSplitter, QVBoxLayout,
#     QFileSystemModel, QTextEdit, QWidget, QMenuBar, QMenu, QAction, QFileDialog,
#     QToolBar, QPushButton, QTabWidget, QToolButton,QComboBox
# )
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QFont, QIcon
# from code_editor import CodeEditor
# from shell import ModernShell


# class IDE(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Window properties
#         self.setWindowTitle("Programers IDE by Ashish")
#         self.setWindowIcon(QIcon("customizable/icons/Sharingan.png"))  # Add your custom icon here
#         self.resize(1200, 800)

#         # Central widget setup
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)

#         # Layout for the central widget
#         self.layout = QVBoxLayout()
#         self.central_widget.setLayout(self.layout)

#         # Splitter to divide file tree and editor
#         self.splitter = QSplitter(Qt.Horizontal)
#         self.layout.addWidget(self.splitter)

#         # Left Toolbar (Vertical)
#         self.toolbar = QToolBar(self)
#         self.toolbar.setOrientation(Qt.Vertical)
#         self.toolbar.setStyleSheet("""
#             QToolBar {
#                 background-color: #21252b;
#                 border: none;
#                 padding: 5px;
#                 border-radius: 6px;
#             }
#             QToolBar::item {
#                 padding: 10px 15px;  /* Add padding for more height and width */
#                 margin: 8px 0;      /* Add margin for spacing between items */
#                 background-color: transparent; /* Ensure background remains clean */
#             }
#             QToolBar::item:hover {
#                 background-color: #3e4451;
#                 border-radius: 4px;
#             }
#         """)
#         self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

#         open_action = QAction(QIcon("customizable/icons/folder.png"), "Explorer (Ctrl+Shift+K)", self)
#         open_action.triggered.connect(self.open_file)
#         self.toolbar.addAction(open_action)

#         # self.toolbar.addSeparator()

#         git_action = QAction(QIcon("customizable/icons/git.png"), "Git", self)
#         # git_action.triggered.connect(self.git_file)
#         self.toolbar.addAction(git_action)

#         # self.toolbar.addSeparator()

#         bug_action = QAction(QIcon("customizable/icons/bug.png"), "Debug", self)
#         # bug_action.triggered.connect(self.bug_file)
#         self.toolbar.addAction(bug_action)

#         # self.toolbar.addSeparator()

#         extension_action = QAction(QIcon("customizable/icons/extension.png"), "Etensions", self)
#         # git_action.triggered.connect(self.extension_file)
#         self.toolbar.addAction(extension_action)

#         # Adjust tool button size manually
#         for action in self.toolbar.actions():
#             button = self.toolbar.widgetForAction(action)
#             if isinstance(button, QToolButton):
#                 button.setFixedSize(60, 60)  # Set width=100px and height=60px


#         # File tree view
#         self.file_tree = QTreeView()
#         self.file_model = QFileSystemModel()
#         self.file_model.setRootPath("Code_Editor")  # Set to root or a specific directory
#         self.file_tree.setModel(self.file_model)
#         self.file_tree.setRootIndex(self.file_model.index("E:\Learnings_and_Projects\GitHub-repo\Code_Editor"))  # Set to root or a specific directory
#         self.file_tree.setHeaderHidden(True)
#         self.file_tree.setColumnHidden(1, True)
#         self.file_tree.setColumnHidden(2, True)
#         self.file_tree.setColumnHidden(3, True)
#         self.file_tree.setStyleSheet("""
#             QTreeView {
#                 background-color: #21252b;
#                 color: #dcdcdc;
#                 border: none;
#                 padding: 5px;
#                 border-radius: 6px;
#             }
#             QTreeView::item:hover {
#                 background-color: #3e4451;
#                 border-radius: 4px;
#             }
#             QTreeView::item {
#                 height: 35px;
#             }
#             QTreeView::item:selected {
#                 background-color: #61afef;
#                 color: #ffffff;
#                 border-radius: 4px;
#             }
#         """)
#         self.file_tree.clicked.connect(self.open_file_from_tree)
#         self.splitter.addWidget(self.file_tree)


#         # Tab widget for editor
#         self.tab_widget = QTabWidget()
#         self.tab_widget.setTabsClosable(True)
#         self.tab_widget.setStyleSheet("""
#             QTabWidget::pane {
#                 border: 1px solid #3e4451;
#                 border-radius: 6px;
#             }
#             QTabBar::tab {
#                 background: #21252b;
#                 color: #abb2bf;
#                 padding: 6px;
#                 border: 1px solid #3e4451;
#                 border-radius: 4px;
#                 margin: 2px;
#             }
#             QTabBar::tab:selected {
#                 background: #61afef;
#                 color: #ffffff;
#             }
#         """)
#         self.tab_widget.tabCloseRequested.connect(self.close_tab)
#         self.splitter.addWidget(self.tab_widget)
#         self.splitter.setSizes([300, 900])
#         # Tab styling update
#         self.tab_widget.setStyleSheet("""
#             QTabWidget::pane {
#                 border: 1px solid #3e4451;
#                 border-radius: 6px;
#             }
#             QTabBar::tab {
#                 min-width: 55px;
#                 background: #21252b;
#                 color: #abb2bf;
#                 padding: 8px 5px;
#                 border: 1px solid #3e4451;
#                 border-radius: 4px;
#                 margin: 6px;
#             }
#             QTabBar::tab:selected {
#                 background: #61afef;
#                 color: #ffffff;
#                 font-weight: bold;
#             }
#             QTabBar::tab:hover {
#                 background: #3e4451;
#                 color: #ffffff;
#             }
#             QTabBar::close-button {
#                 image: url('customizable/icons/closs.png'); /* Replace with your close icon path */
#             }
#         """)

#         # Code editor
#         self.editor = CodeEditor()
#         self.splitter.addWidget(self.editor)
#         self.splitter.setSizes([300, 900])
#         self.editor.setStyleSheet("""
#             QTextEdit {
#                 background-color: #282c34;
#                 color: #abb2bf;
#                 border: 1px solid #3e4451;
#                 border-radius: 6px;
#                 padding: 8px;
#            }
#             QTextEdit:focus {
#                 border: 1px solid #61afef;
#             }
#             QPlainTextEdit {
#                 background-color: #282c34;
#                 color: #abb2bf;
#                 border: 1px solid #3e4451;
#                 border-radius: 6px;
#                 padding: 8px;                      
#             }
#             QPlainTextEdit:hover {
#                 border: 1px solid #61afef;                      
#             }
#         """)
#         # Shell
#         self.shell = ModernShell()
#         self.splitter.addWidget(self.shell)
#         self.splitter.setSizes([300, 900])

#         # Language selector
#         self.language_selector = QComboBox()
#         self.language_selector.addItems(["Python", "JavaScript"])
#         self.language_selector.currentTextChanged.connect(self.changeLanguage)
#         self.layout.addWidget(self.language_selector)

#         # Menu bar setup
#         self.menu_bar = QMenuBar()
#         self.setMenuBar(self.menu_bar)
#         self.menu_bar.setStyleSheet("""
#             QMenuBar {
#                 background-color: #21252b;
#                 color: #abb2bf;
#                 border: none;
#             }
#             QMenuBar::item:hover {
#                 background-color: #3e4451;
#                 border-radius: 4px;
#             }
#             QMenuBar::item:selected {
#                 background-color: #61afef;
#                 color: #ffffff;
#                 border-radius: 4px;
#             }
#         """)

#         file_menu = QMenu("File", self)
#         self.menu_bar.addMenu(file_menu)

#         new_action_menu = QAction(QIcon("icons/new_file.png"), "New", self)  # Add icons if available
#         new_action_menu.triggered.connect(self.open_file)
#         file_menu.addAction(new_action_menu)

#         open_action_menu = QAction(QIcon("icons/open.png"), "Open", self)
#         open_action_menu.triggered.connect(self.open_file)
#         file_menu.addAction(open_action_menu)

#         save_action_menu = QAction(QIcon("icons/save.png"), "Save", self)
#         save_action_menu.triggered.connect(self.save_file)
#         file_menu.addAction(save_action_menu)

#         file_menu.addSeparator()

#         exit_action = QAction(QIcon("exit_icon.png"), "Exit", self)
#         exit_action.triggered.connect(self.close)
#         file_menu.addAction(exit_action)

#         # Initialize the current file dictionary
#         self.open_files = {}
    
#     def changeLanguage(self, language):
#         self.editor.setLanguage(language)

#     def open_file(self):
#         file_path, _ = QFileDialog.getOpenFileName(self, "Open File")
#         if file_path:
#             self.load_file(file_path)

#     def save_file(self):
#         current_widget = self.tab_widget.currentWidget()
#         if current_widget:
#             editor, file_path = self.open_files.get(self.tab_widget.indexOf(current_widget))
#             if file_path:
#                 with open(file_path, "w") as file:
#                     file.write(editor.toPlainText())
#             else:
#                 file_path, _ = QFileDialog.getSaveFileName(self, "Save File")
#                 if file_path:
#                     with open(file_path, "w") as file:
#                         file.write(editor.toPlainText())

#     def load_file(self, file_path):
#         if file_path not in [path for _, path in self.open_files.values()]:
#             try:
#                 with open(file_path, "r") as file:
#                     content = file.read()

#                 editor = CodeEditor()
#                 editor.setPlainText(content)

#                 # Ensure consistent styling for the editor
#                 editor.setStyleSheet("""
#                     QTextEdit, QPlainTextEdit {
#                         background-color: #282c34;
#                         color: #abb2bf;
#                         border: 1px solid #3e4451;
#                         border-radius: 6px;
#                         padding: 8px;
#                     }
#                     QTextEdit:focus, QPlainTextEdit:hover {
#                         border: 1px solid #61afef;
#                     }
#                 """)

#                 file_name = file_path.split("/")[-1]
#                 self.tab_widget.addTab(editor, file_name)

#                 # Keep track of open files
#                 self.open_files[self.tab_widget.indexOf(editor)] = (editor, file_path)
#             except Exception as e:
#                 print(f"Error loading file: {e}")

#     def open_file_from_tree(self, index):
#         file_path = self.file_model.filePath(index)
#         if not self.file_model.isDir(index):
#             self.load_file(file_path)

#     def close_tab(self, index):
#         self.tab_widget.removeTab(index)
#         self.open_files.pop(index, None)
        
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
    
#     # Apply the global style to the application
#     app.setStyleSheet("""
#         QWidget {
#             background-color: #282c34;
#         }
#     """)
    
#     ide = IDE()
#     ide.show()
#     sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QTextEdit, QFileDialog, QVBoxLayout, QTreeView, QFileSystemModel, QSplitter,
                             QHBoxLayout, QWidget, QAction, QMenu, QPushButton, QToolBar, QLabel, QInputDialog, QMessageBox)
from PyQt5.QtGui import QFont, QColor, QTextCursor
from PyQt5.QtCore import Qt, QProcess

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IDE with Shell UI")
        self.setGeometry(100, 100, 1200, 800)
        
        self.recent_files = []
        self.init_ui()
        self.init_menubar()
        self.init_toolbar()
        
    def init_ui(self):
        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Splitter for file tree and editor/shell
        self.splitter = QSplitter(Qt.Horizontal, self)
        layout.addWidget(self.splitter)

        # File tree setup
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath("")

        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index(""))
        self.file_tree.doubleClicked.connect(self.open_file_from_tree)
        self.splitter.addWidget(self.file_tree)

        # Tab widget for editors
        self.tabs = QTabWidget()
        self.splitter.addWidget(self.tabs)

        # Shell output widget
        self.shell = QTextEdit()
        self.shell.setReadOnly(True)
        self.shell.setStyleSheet("background-color: black; color: white;")
        self.splitter.addWidget(self.shell)

        self.splitter.setSizes([200, 600, 400])

    def init_menubar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        new_file_action = QAction("New File", self)
        new_file_action.triggered.connect(self.new_file)
        file_menu.addAction(new_file_action)

        open_file_action = QAction("Open File", self)
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction("Save File", self)
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)

        close_tab_action = QAction("Close Tab", self)
        close_tab_action.triggered.connect(self.close_tab)
        file_menu.addAction(close_tab_action)

        # Recent Files menu
        self.recent_files_menu = QMenu("Recent Files", self)
        file_menu.addMenu(self.recent_files_menu)

        set_root_action = QAction("Set Root Directory", self)
        set_root_action.triggered.connect(self.set_root_directory)
        file_menu.addAction(set_root_action)

        self.update_recent_files_menu()

    def init_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        run_action = QAction("Run", self)
        run_action.triggered.connect(self.run_code)
        toolbar.addAction(run_action)

        clear_shell_action = QAction("Clear Shell", self)
        clear_shell_action.triggered.connect(self.clear_shell)
        toolbar.addAction(clear_shell_action)

        theme_action = QAction("Toggle Theme", self)
        theme_action.triggered.connect(self.toggle_theme)
        toolbar.addAction(theme_action)

    def new_file(self):
        editor = QTextEdit()
        index = self.tabs.addTab(editor, "Untitled")
        self.tabs.setCurrentIndex(index)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
        if file_path:
            self.load_file(file_path)

    def save_file(self):
        current_editor = self.tabs.currentWidget()
        if not current_editor:
            return
        
        if hasattr(current_editor, "file_path") and current_editor.file_path:
            with open(current_editor.file_path, "w") as file:
                file.write(current_editor.toPlainText())
            self.tabs.setTabText(self.tabs.currentIndex(), current_editor.file_path.split("/")[-1])
        else:
            self.save_file_as()

    def save_file_as(self):
        current_editor = self.tabs.currentWidget()
        if not current_editor:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "All Files (*.*)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(current_editor.toPlainText())
            current_editor.file_path = file_path
            self.tabs.setTabText(self.tabs.currentIndex(), file_path.split("/")[-1])

    def close_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index != -1:
            self.tabs.removeTab(current_index)

    def load_file(self, file_path):
        with open(file_path, "r") as file:
            content = file.read()
        editor = QTextEdit()
        editor.setPlainText(content)
        editor.file_path = file_path
        index = self.tabs.addTab(editor, file_path.split("/")[-1])
        self.tabs.setCurrentIndex(index)

        if file_path not in self.recent_files:
            self.recent_files.append(file_path)
        self.update_recent_files_menu()

    def update_recent_files_menu(self):
        self.recent_files_menu.clear()
        for file_path in self.recent_files[-5:]:
            action = QAction(file_path, self)
            action.triggered.connect(lambda checked, path=file_path: self.load_file(path))
            self.recent_files_menu.addAction(action)

    def set_root_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Root Directory")
        if dir_path:
            self.file_model.setRootPath(dir_path)
            self.file_tree.setRootIndex(self.file_model.index(dir_path))

    def open_file_from_tree(self, index):
        file_path = self.file_model.filePath(index)
        if not self.file_model.isDir(index):
            self.load_file(file_path)

    def run_code(self):
        current_editor = self.tabs.currentWidget()
        if not current_editor:
            return
        
        code = current_editor.toPlainText()
        with open("temp_code.py", "w") as file:
            file.write(code)

        process = QProcess(self)
        process.readyReadStandardOutput.connect(lambda: self.shell.append(process.readAllStandardOutput().data().decode()))
        process.readyReadStandardError.connect(lambda: self.shell.append(process.readAllStandardError().data().decode()))
        process.start("python", ["temp_code.py"])

    def clear_shell(self):
        self.shell.clear()

    def toggle_theme(self):
        if self.shell.styleSheet() == "background-color: black; color: white;":
            self.shell.setStyleSheet("background-color: white; color: black;")
        else:
            self.shell.setStyleSheet("background-color: black; color: white;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ide = IDE()
    ide.show()
    sys.exit(app.exec_())
