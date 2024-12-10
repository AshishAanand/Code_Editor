from PyQt5.QtGui import QTextCharFormat, QColor, QFont
from PyQt5.QtGui import QSyntaxHighlighter
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document, language="python", theme="monokai"):
        super().__init__(document)
        self.language = language
        self.theme = theme
        try:
            self.lexer = get_lexer_by_name(self.language)
        except Exception as e:
            raise ValueError(f"Error initializing lexer: {e}")
        try:
            self.style = get_style_by_name(self.theme)
        except Exception as e:
            raise ValueError(f"Error initializing style: {e}")
        self.format_rules = self.build_format_rules()

    def build_format_rules(self):
        """
        Build text formats based on Pygments token styles.
        """
        rules = {}
        for token, style in self.style.styles.items():
            # Skip if `style` is None or not dictionary-like
            if not style or not isinstance(style, dict):
                print(f"Skipping token {token}: Invalid style format.")
                continue

            text_format = QTextCharFormat()
            try:
                # Apply foreground color
                color = style.get('color')
                if color:
                    text_format.setForeground(QColor(f"#{color}"))
                # Apply background color
                bgcolor = style.get('bgcolor')
                if bgcolor:
                    text_format.setBackground(QColor(f"#{bgcolor}"))
                # Apply bold font
                if style.get('bold', False):
                    text_format.setFontWeight(QFont.Bold)
                # Apply italic font
                if style.get('italic', False):
                    text_format.setFontItalic(True)
                # Apply underline
                if style.get('underline', False):
                    text_format.setFontUnderline(True)
            except Exception as e:
                print(f"Error processing style for token {token}: {e}")
                continue

            rules[token] = text_format
        return rules

    def highlightBlock(self, text):
        """
        Apply syntax highlighting to a block of text.
        """
        try:
            for token, content in lex(text, self.lexer):
                if token in self.format_rules:
                    start = 0
                    while True:
                        start = text.find(content, start)
                        if start == -1:
                            break
                        length = len(content)
                        self.setFormat(start, length, self.format_rules[token])
                        start += length
        except Exception as e:
            print(f"Error during highlighting: {e}")
