from PyQt5.QtWidgets import QApplication, QTextEdit
from syntax_highlighter import SyntaxHighlighter

app = QApplication([])
editor = QTextEdit()
highlighter = SyntaxHighlighter(editor.document(), language="python", theme="monokai")
editor.setText("def test_function():\n    print('Syntax highlighting!')")
editor.show()
app.exec_()
