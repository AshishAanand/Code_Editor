from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegularExpression
import ast

class BaseHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlightingRules = []
        self.errorFormat = QTextCharFormat()  # Initialize the errorFormat
        self.errorFormat.setUnderlineColor(QColor("red"))
        self.errorFormat.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

    def addRule(self, pattern, format):
        """Add a single highlighting rule."""
        regex = QRegularExpression(pattern)
        self.highlightingRules.append((regex, format))

    def highlightBlock(self, text):
        # Apply syntax highlighting rules
        for pattern, text_format in self.highlightingRules:
            match = pattern.globalMatch(text)
            while match.hasNext():
                match_range = match.next()
                start = match_range.capturedStart()
                length = match_range.capturedLength()
                self.setFormat(start, length, text_format)

        # Highlight errors
        errors = detect_errors(text)
        for start, length in errors:
            self.setFormat(start, length, self.errorFormat)


def detect_errors(text):
    try:
        ast.parse(text)  # Parse the Python code to detect syntax errors
        return []  # No errors
    except SyntaxError as e:
        start = e.offset - 1 if e.offset else 0  # Adjust for 0-based indexing
        return [(start, len(e.text.strip()))]  # Return error position


def createFormat(color, bold=False, italic=False):
    """Utility to create text formats."""
    text_format = QTextCharFormat()
    text_format.setForeground(QColor(color))
    if bold:
        text_format.setFontWeight(QFont.Bold)
    if italic:
        text_format.setFontItalic(True)
    return text_format


class PythonHighlighter(BaseHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # Define formats
        keyword_format = createFormat("#0000FF", bold=True)
        comment_format = createFormat("#00AA00", italic=True)
        string_format = createFormat("#AA5500")
        number_format = createFormat("#FF00FF")

        # Define patterns
        keywords = r"\b(?:def|class|if|else|elif|while|for|import|from|return)\b"
        comments = r"#.*"
        strings = r"\".*?\"|'.*?'"
        numbers = r"\b\d+\b"

        # Add rules
        self.addRule(keywords, keyword_format)
        self.addRule(comments, comment_format)
        self.addRule(strings, string_format)
        self.addRule(numbers, number_format)


class JavaScriptHighlighter(BaseHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # Define formats
        keyword_format = createFormat("#0000FF", bold=True)
        comment_format = createFormat("#00AA00", italic=True)
        string_format = createFormat("#AA5500")
        number_format = createFormat("#FF00FF")

        # Define patterns
        keywords = r"\b(?:function|var|let|const|if|else|return|for|while)\b"
        single_line_comment = r"//.*"
        multi_line_comment = r"/\*.*?\*/"
        strings = r"\".*?\"|'.*?'"
        numbers = r"\b\d+\b"

        # Add rules
        self.addRule(keywords, keyword_format)
        self.addRule(single_line_comment, comment_format)
        self.addRule(multi_line_comment, comment_format)
        self.addRule(strings, string_format)
        self.addRule(numbers, number_format)
