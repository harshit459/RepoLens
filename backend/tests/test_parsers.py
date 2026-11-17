import unittest

from backend.app.parsers.python_parser import PythonParser
from backend.app.parsers.javascript_parser import JavaScriptParser
from backend.app.parsers.html_parser import HTMLParser
from backend.app.parsers.css_parser import CSSParser


class TestParsers(unittest.TestCase):

    def check_common_schema(self, result):
        self.assertIn("language", result)
        self.assertIn("entities", result)
        self.assertIn("relationships", result)
        self.assertIn("errors", result)

        for entity in result["entities"]:
            self.assertIn("name", entity)
            self.assertIn("type", entity)
            self.assertIn("language", entity)
            self.assertIn("file_path", entity)
            self.assertIn("start_line", entity)
            self.assertIn("end_line", entity)
            self.assertIn("metadata", entity)

    def test_python_parser(self):
        parser = PythonParser()

        source = """
def calculate(a, b):
    return a + b

class Calculator:
    def multiply(self, a, b):
        return a * b
"""

        result = parser.parse(source, file_path="main.py")

        self.check_common_schema(result)

        names = [entity["name"] for entity in result["entities"]]

        self.assertIn("calculate", names)
        self.assertIn("Calculator", names)
        self.assertIn("multiply", names)

        self.assertEqual(result["errors"], [])

    def test_javascript_parser(self):
        parser = JavaScriptParser()

        source = """
function greet(name) {
    return "Hello " + name;
}
"""

        result = parser.parse(source, file_path="app.js")

        self.check_common_schema(result)

        names = [entity["name"] for entity in result["entities"]]

        self.assertIn("greet", names)
        self.assertEqual(result["errors"], [])

    def test_html_parser(self):
        parser = HTMLParser()

        source = """
<div class="container">
    <h1>Hello</h1>
    <button type="submit">Click</button>
</div>
"""

        result = parser.parse(source, file_path="index.html")

        self.check_common_schema(result)

        entities = result["entities"]

        names = [entity["name"] for entity in entities]

        self.assertIn("div", names)
        self.assertIn("h1", names)
        self.assertIn("button", names)

        div = next(e for e in entities if e["name"] == "div")

        self.assertEqual(
            div["metadata"]["attributes"]["class"],
            "container"
        )

        self.assertEqual(result["errors"], [])

    def test_css_parser(self):
        parser = CSSParser()

        source = """
.container {
    display: flex;
    padding: 20px;
}

button {
    background-color: blue;
}
"""

        result = parser.parse(source, file_path="style.css")

        self.check_common_schema(result)

        entities = result["entities"]

        names = [entity["name"] for entity in entities]

        self.assertIn(".container", names)
        self.assertIn("button", names)

        container = next(
            e for e in entities if e["name"] == ".container"
        )

        declarations = container["metadata"]["declarations"]

        properties = [d["property"] for d in declarations]

        self.assertIn("display", properties)
        self.assertIn("padding", properties)

        self.assertEqual(result["errors"], [])


if __name__ == "__main__":
    unittest.main()