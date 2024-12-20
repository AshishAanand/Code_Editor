import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTreeView, QSplitter, QVBoxLayout,
    QFileSystemModel, QTextEdit, QWidget, QMenuBar, QMenu, QAction, QFileDialog,
    QToolBar, QPushButton, QTabWidget, QToolButton,QComboBox, QLabel, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from code_editor import CodeEditor
from shell import ModernShell
import os

from lsp_server import LSPClient

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("Programers IDE by Ashish")
        self.setWindowIcon(QIcon("customizable/icons/Sharingan.png"))  # Add your custom icon here
        self.resize(1200, 800)
        # Create a status bar
        self.status_bar = self.statusBar()
        self.language_label = QLabel("Language: Unknown")
        self.status_bar.addPermanentWidget(self.language_label)

        # Current file path
        self.current_file = None

        self.language_label.setStyleSheet("""
            color: white;
            margin: 5px 32px;
        """)
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


        # Configure file tree view
        self.file_tree = QTreeView()
        self.file_model = QFileSystemModel()

        # Set initial root path
        initial_path = "E:/Learnings_and_Projects/GitHub-repo/Code_Editor"
        self.file_model.setRootPath(initial_path)
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index(initial_path))

        # Header configuration
        self.file_tree.header().setSectionResizeMode(QHeaderView.Stretch)
        self.file_tree.setHeaderHidden(False)
        self.update_header_label(initial_path)

        # Hide unnecessary columns
        self.file_tree.setColumnHidden(1, True)
        self.file_tree.setColumnHidden(2, True)
        self.file_tree.setColumnHidden(3, True)

        # Define file opening logic
        
                

        # Connect file selection to open files
        self.file_tree.clicked.connect(self.open_file_from_tree)

        # Style the file tree
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

        self.file_tree.header().setStyleSheet("""
            QHeaderView::section {
                background-color: #3e4451;
                color: #dcdcdc;
                padding: 4px;
                border: 1px solid #21252b;
            }
        """)

        # Add the file tree to the layout
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
        # path = os.access("C:/Users/HP/AppData/Roaming/npm/pyright", os.X_OK)
        # print(path)
        # self.lsp_client = LSPClient(language_server_path="C:/Users/HP/AppData/Roaming/npm/pyright", root_path=os.getcwd())

        # # Connect signals
        # self.lsp_client.response_received.connect(self.handle_lsp_response)
        # self.editor.text_changed.connect(self.handle_text_change)

        # # Start LSP client
        # self.lsp_client.start()
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
        # Shell
        self.shell = ModernShell()
        self.splitter.addWidget(self.shell)
        self.splitter.setSizes([300, 900])

        # Language selector
        # self.language_selector = QComboBox()
        # self.language_selector.addItems(["Python", "JavaScript"])
        # self.language_selector.currentTextChanged.connect(self.changeLanguage)
        # self.layout.addWidget(self.language_selector)

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

        # Add a "Run" button
        run_button = QPushButton("Run")
        run_button.clicked.connect(self.run_code)
        self.toolbar.addWidget(run_button)

        # Initialize the current file dictionary
        self.open_files = {}

    
    def changeLanguage(self, language):
        self.editor.setLanguage(language)
    
    def handle_text_change(self, text):
        """Handle editor text changes by sending to LSP for suggestions."""
        message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "textDocument/completion",
            "params": {
                "textDocument": {"uri": "file://example.py"},
                "position": {
                    "line": self.editor.textCursor().blockNumber(),
                    "character": self.editor.textCursor().positionInBlock(),
                },
            },
        }
        self.lsp_client.send_message(message)

    def handle_lsp_response(self, response):
        """Process LSP responses for autocomplete."""
        if "id" in response and response["id"] == 2:  # Completion response
            suggestions = [
                item["label"] for item in response.get("result", {}).get("items", [])
            ]
            self.editor.autocomplete.update_suggestions(suggestions)

    def closeEvent(self, event):
        """Clean up the LSP process when the editor closes."""
        self.lsp_client.stop()
        super().closeEvent(event)
    
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File")
        if file_path:
            self.load_file(file_path)
            # Detect language
            detected_language = self.shell.detect_language(file_path)
            # Update status bar
            self.language_label.setText(f"Language: {detected_language}")
            self.current_file = os.path.basename(file_path)
            print(self.current_file)

    def run_code(self):
        if self.current_file:
            # Load the code from the editor for execution
            current_widget = self.tab_widget.currentWidget()
            if current_widget:
                code = current_widget.toPlainText()  # Get the code from the current editor
                self.shell.run_code(self.current_file, code)
        else:
            print("No file selected to run.")

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
                    self.code = file.read()

                editor = CodeEditor()
                editor.setPlainText(self.code)

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

    # def open_file_from_tree(self, index):
    #     file_path = self.file_model.filePath(index)
    #     if not self.file_model.isDir(index):
    #         self.load_file(file_path)
            
    def close_tab(self, index):
        self.tab_widget.removeTab(index)
        self.open_files.pop(index, None)

    # def run_code(self):
    #     if self.current_file:
    #         self.shell.run_code(self.current_file, self.code)
    #     else:
    #         print("No file selected to run.")

    def update_header_label(self, path):
        """Update the header label with the current folder name."""
        folder_name = os.path.basename(path) or path  # Handle cases like root drives
        self.file_model.setHeaderData(0, Qt.Horizontal, folder_name)

    def open_file_from_tree(self, index):
        path = self.file_model.filePath(index)
        if os.path.isfile(path):
            self.load_file(path)  # Placeholder function to load file into the editor
        elif os.path.isdir(path):
            self.file_tree.setRootIndex(self.file_model.index(path))  # Change root to folder
            self.update_header_label(path)  # Update header with folder name
            self.current_file = os.path.basename(path)
        
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
