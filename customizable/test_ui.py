import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTreeView, QSplitter, QVBoxLayout,
    QFileSystemModel, QTextEdit, QWidget, QMenuBar, QMenu, QAction, QFileDialog,
    QToolBar, QPushButton, QTabWidget, QToolButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from code_editor import CodeEditor


class IDE(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("Programers IDE by Ashish")
        self.setWindowIcon(QIcon("customizable/icons/Sharingan.png"))  # Add your custom icon here
        self.resize(1200, 800)

        # Central widget setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout for the central widget
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Splitter to divide file tree and editor
        self.splitter = QSplitter(Qt.Horizontal)
        self.layout.addWidget(self.splitter)

        # Left Toolbar (Vertical)
        self.toolbar = QToolBar(self)
        self.toolbar.setOrientation(Qt.Vertical)
        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: #21252b;
                border: none;
                padding: 5px;
                border-radius: 6px;
            }
            QToolBar::item {
                padding: 10px 15px;  /* Add padding for more height and width */
                margin: 8px 0;      /* Add margin for spacing between items */
                background-color: transparent; /* Ensure background remains clean */
            }
            QToolBar::item:hover {
                background-color: #3e4451;
                border-radius: 4px;
            }
        """)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        open_action = QAction(QIcon("customizable/icons/folder.png"), "Explorer (Ctrl+Shift+K)", self)
        open_action.triggered.connect(self.open_file)
        self.toolbar.addAction(open_action)

        # self.toolbar.addSeparator()

        git_action = QAction(QIcon("customizable/icons/git.png"), "Git", self)
        # git_action.triggered.connect(self.git_file)
        self.toolbar.addAction(git_action)

        # self.toolbar.addSeparator()

        bug_action = QAction(QIcon("customizable/icons/bug.png"), "Debug", self)
        # bug_action.triggered.connect(self.bug_file)
        self.toolbar.addAction(bug_action)

        # self.toolbar.addSeparator()

        extension_action = QAction(QIcon("customizable/icons/extension.png"), "Etensions", self)
        # git_action.triggered.connect(self.extension_file)
        self.toolbar.addAction(extension_action)

        # Adjust tool button size manually
        for action in self.toolbar.actions():
            button = self.toolbar.widgetForAction(action)
            if isinstance(button, QToolButton):
                button.setFixedSize(60, 60)  # Set width=100px and height=60px


        # File tree view
        self.file_tree = QTreeView()
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath("Code_Editor")  # Set to root or a specific directory
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index("E:\Learnings_and_Projects\GitHub-repo\Code_Editor"))  # Set to root or a specific directory
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setColumnHidden(1, True)
        self.file_tree.setColumnHidden(2, True)
        self.file_tree.setColumnHidden(3, True)
        self.file_tree.setStyleSheet("""
            QTreeView {
                background-color: #21252b;
                color: #dcdcdc;
                border: none;
                padding: 5px;
                border-radius: 6px;
            }
            QTreeView::item:hover {
                background-color: #3e4451;
                border-radius: 4px;
            }
            QTreeView::item {
                height: 35px;
            }
            QTreeView::item:selected {
                background-color: #61afef;
                color: #ffffff;
                border-radius: 4px;
            }
        """)
        self.file_tree.clicked.connect(self.open_file_from_tree)
        self.splitter.addWidget(self.file_tree)


        # Tab widget for editor
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3e4451;
                border-radius: 6px;
            }
            QTabBar::tab {
                background: #21252b;
                color: #abb2bf;
                padding: 6px;
                border: 1px solid #3e4451;
                border-radius: 4px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #61afef;
                color: #ffffff;
            }
        """)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.splitter.addWidget(self.tab_widget)
        self.splitter.setSizes([300, 900])
        # Tab styling update
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3e4451;
                border-radius: 6px;
            }
            QTabBar::tab {
                min-width: 55px;
                background: #21252b;
                color: #abb2bf;
                padding: 8px 5px;
                border: 1px solid #3e4451;
                border-radius: 4px;
                margin: 6px;
            }
            QTabBar::tab:selected {
                background: #61afef;
                color: #ffffff;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #3e4451;
                color: #ffffff;
            }
            QTabBar::close-button {
                image: url('customizable/icons/closs.png'); /* Replace with your close icon path */
            }
        """)

        # Code editor
        self.editor = CodeEditor()
        self.splitter.addWidget(self.editor)
        self.splitter.setSizes([300, 900])
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #282c34;
                color: #abb2bf;
                border: 1px solid #3e4451;
                border-radius: 6px;
                padding: 8px;
           }
            QTextEdit:focus {
                border: 1px solid #61afef;
            }
            QPlainTextEdit {
                background-color: #282c34;
                color: #abb2bf;
                border: 1px solid #3e4451;
                border-radius: 6px;
                padding: 8px;                      
            }
            QPlainTextEdit:hover {
                border: 1px solid #61afef;                      
            }
        """)

        # Menu bar setup
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)
        self.menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #21252b;
                color: #abb2bf;
                border: none;
            }
            QMenuBar::item:hover {
                background-color: #3e4451;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #61afef;
                color: #ffffff;
                border-radius: 4px;
            }
        """)

        file_menu = QMenu("File", self)
        self.menu_bar.addMenu(file_menu)

        new_action_menu = QAction(QIcon("icons/new_file.png"), "New", self)  # Add icons if available
        new_action_menu.triggered.connect(self.open_file)
        file_menu.addAction(new_action_menu)

        open_action_menu = QAction(QIcon("icons/open.png"), "Open", self)
        open_action_menu.triggered.connect(self.open_file)
        file_menu.addAction(open_action_menu)

        save_action_menu = QAction(QIcon("icons/save.png"), "Save", self)
        save_action_menu.triggered.connect(self.save_file)
        file_menu.addAction(save_action_menu)

        file_menu.addSeparator()

        exit_action = QAction(QIcon("exit_icon.png"), "Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Initialize the current file dictionary
        self.open_files = {}

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if file_path:
            self.load_file(file_path)

    def save_file(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget:
            editor, file_path = self.open_files.get(self.tab_widget.indexOf(current_widget))
            if file_path:
                with open(file_path, "w") as file:
                    file.write(editor.toPlainText())
            else:
                file_path, _ = QFileDialog.getSaveFileName(self, "Save File")
                if file_path:
                    with open(file_path, "w") as file:
                        file.write(editor.toPlainText())

    def load_file(self, file_path):
        if file_path not in [path for _, path in self.open_files.values()]:
            try:
                with open(file_path, "r") as file:
                    content = file.read()

                editor = CodeEditor()
                editor.setPlainText(content)

                # Ensure consistent styling for the editor
                editor.setStyleSheet("""
                    QTextEdit, QPlainTextEdit {
                        background-color: #282c34;
                        color: #abb2bf;
                        border: 1px solid #3e4451;
                        border-radius: 6px;
                        padding: 8px;
                    }
                    QTextEdit:focus, QPlainTextEdit:hover {
                        border: 1px solid #61afef;
                    }
                """)

                file_name = file_path.split("/")[-1]
                self.tab_widget.addTab(editor, file_name)

                # Keep track of open files
                self.open_files[self.tab_widget.indexOf(editor)] = (editor, file_path)
            except Exception as e:
                print(f"Error loading file: {e}")

    def open_file_from_tree(self, index):
        file_path = self.file_model.filePath(index)
        if not self.file_model.isDir(index):
            self.load_file(file_path)

    def close_tab(self, index):
        self.tab_widget.removeTab(index)
        self.open_files.pop(index, None)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply the global style to the application
    app.setStyleSheet("""
        QWidget {
            background-color: #282c34;
        }
    """)
    
    ide = IDE()
    ide.show()
    sys.exit(app.exec_())