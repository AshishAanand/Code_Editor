from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from ui_test import Ui_MainWindow


class CodeEditorWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_functionality()

    def init_functionality(self):
        # Add a menu for selecting languages
        language_menu = self.menuFile.addMenu('Language')

        languages = ["python", "javascript", "html", "css", "c", "cpp"]
        for lang in languages:
            lang_action = QAction(lang.capitalize(), self)
            lang_action.triggered.connect(lambda checked, l=lang: self.change_language(l))
            language_menu.addAction(lang_action)

        # Additional setup if needed
        self.setWindowTitle("Code Editor")

    def change_language(self, language):
        self.workspace.set_language(language)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    editor_window = CodeEditorWindow()
    editor_window.show()
    sys.exit(app.exec_())
