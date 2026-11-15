import tree_sitter_python as tspython

from tree_sitter import Language, Parser
from .base import BaseParser


class PythonParser(BaseParser):

    def __init__(self):
        language = Language(tspython.language())
        self.parser = Parser(language)

    def parse(self, source_code: str) -> dict:

        tree = self.parser.parse(source_code.encode("utf8"))

        metadata = {
            "language": "python",
            "functions": [],
            "classes": []
        }

        def traverse(node, current_class=None):

            if node.type == "class_definition":

                name_node = node.child_by_field_name("name")
                current_class = name_node.text.decode("utf8")

                metadata["classes"].append({
                    "name": current_class,
                    "start_line": node.start_point.row + 1,
                    "end_line": node.end_point.row + 1
                })

            if node.type == "function_definition":

                name_node = node.child_by_field_name("name")
                params_node = node.child_by_field_name("parameters")

                parameters = []

                if params_node:
                    for param in params_node.named_children:
                        parameters.append(param.text.decode("utf8"))

                metadata["functions"].append({
                    "name": name_node.text.decode("utf8"),
                    "type": "method" if current_class else "function",
                    "class_name": current_class,
                    "parameters": parameters,
                    "start_line": node.start_point.row + 1,
                    "end_line": node.end_point.row + 1
                })

            for child in node.named_children:
                traverse(child, current_class)

        traverse(tree.root_node)

        return metadata