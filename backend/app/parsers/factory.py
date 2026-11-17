from pathlib import Path

from .python_parser import PythonParser
from .javascript_parser import JavaScriptParser
from .html_parser import HTMLParser
from .css_parser import CSSParser

class ParserFactory:

    PARSERS = {
        ".py": PythonParser,
        ".js": JavaScriptParser,
        ".jsx": JavaScriptParser,
        ".html": HTMLParser,
        ".css": CSSParser
    }

    @classmethod
    def get_parser(cls, file_path: str):

        extension = Path(file_path).suffix.lower()

        parser_class = cls.PARSERS.get(extension)

        if parser_class is None:
            return None

        return parser_class()