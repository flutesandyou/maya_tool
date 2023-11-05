import re
from PySide2.QtCore import QRegExp, Qt
from PySide2.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter, QFont

class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(PythonSyntaxHighlighter, self).__init__(parent)

        # Define the syntax highlight rules
        self.highlight_rules = [
            (QRegExp(r'\bTrue\b|\bFalse\b|\b(if|else|elif|while|for|in|return|import|from|as|not|and|or)\b'), 'keyword_format'),  # Keywords: True, False, and other Python keywords
            (QRegExp(r'\b(def|class)\b'), 'keyword_format2'),
            (QRegExp(r'\b(None|self)\b'), 'special_format'),  # Special objects: None and self
            (QRegExp(r'#[^\n]*'), 'comment_format'),  # Comments
            (QRegExp(r'".*?"'), 'double_quote_string_format'),  # Double-quoted strings
            (QRegExp(r"'.*?'"), 'single_quote_string_format'),  # Single-quoted strings
        ]

        self.formats = {
            'keyword_format': QTextCharFormat(),
            'keyword_format2': QTextCharFormat(),
            'special_format': QTextCharFormat(),
            'comment_format': QTextCharFormat(),
            'double_quote_string_format': QTextCharFormat(),
            'single_quote_string_format': QTextCharFormat(),
            'method_def_format': QTextCharFormat(),
            'class_name_format' : QTextCharFormat(),
        }

        # Set the format for various syntax elements (existing format settings)

        # Set the format for method definitions (e.g., def METHODNAME)
        method_def_format = self.formats['method_def_format']
        method_def_format.setForeground(QColor(210, 180, 140))  # Light blue color for regular method definitions

        keyword_format = self.formats['keyword_format']
        keyword_format.setForeground(QColor(188, 137, 189)) 

        keyword_format2 = self.formats['keyword_format2']
        keyword_format2.setForeground(QColor(103, 154, 198)) 

        # Set the format for Python keywords (including "def" keyword)
        class_name_format = self.formats['class_name_format']
        class_name_format.setForeground(QColor(113, 198, 177))  

        comment_format = self.formats['comment_format']
        comment_format.setForeground(QColor(116,152,93))

        # Define the rule patterns and formats
        self.highlight_rules_and_formats = [(QRegExp(pattern), format_name) for pattern, format_name in self.highlight_rules]

    def highlightBlock(self, text):
        for pattern, format_name in self.highlight_rules_and_formats:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, self.formats[format_name])
                index = expression.indexIn(text, index + length)

        # Highlight method definitions using the Python re module
        method_def_format = self.formats['method_def_format']
        method_def_pattern = r'\bdef\s+(\w+)\b'  # Pattern for finding method definitions
        for match in re.finditer(method_def_pattern, text):
            start, end = match.span(0)  # Get the span of the entire match (including "def" and method name)
            self.setFormat(start, end - start, method_def_format)

            # Highlight the "def" keyword with the Python keyword format
            self.setFormat(start, 3, self.formats['keyword_format2'])  # The "def" keyword is 3 characters long
            
        class_name_format = self.formats['class_name_format']
        class_name_pattern = r'\bclass\s+(\w+)\s*[:\(]'
        for match in re.finditer(class_name_pattern, text):
            start, end = match.span(1)  # Get the span of the class name (group 1)
            self.setFormat(start, end - start, class_name_format)
