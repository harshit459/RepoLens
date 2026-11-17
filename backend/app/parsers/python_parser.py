import tree_sitter_python as tspython
from tree_sitter import Language, Parser

from .base import BaseParser
from .schema import create_entity, create_parse_result


class PythonParser(BaseParser):

    def __init__(self):
        language = Language(tspython.language())
        self.parser = Parser(language)

    def parse(self, source_code: str, file_path=None) -> dict:

        tree = self.parser.parse(source_code.encode("utf8"))

        entities = []

        def traverse(node, current_class=None):

            if node.type == "class_definition":

                name_node = node.child_by_field_name("name")

                if name_node:
                    class_name = name_node.text.decode("utf8")

                    entities.append(
                        create_entity(
                            name=class_name,
                            entity_type="class",
                            language="python",
                            file_path=file_path,
                            start_line=node.start_point.row + 1,
                            end_line=node.end_point.row + 1,
                            metadata={}
                        )
                    )

                    for child in node.named_children:
                        traverse(child, current_class=class_name)

                    return

            elif node.type == "function_definition":

                name_node = node.child_by_field_name("name")
                parameters_node = node.child_by_field_name("parameters")

                if name_node:

                    function_name = name_node.text.decode("utf8")

                    parameters = []

                    if parameters_node:
                        parameters = [
                            child.text.decode("utf8")
                            for child in parameters_node.named_children
                        ]

                    entity_type = (
                        "method" if current_class else "function"
                    )

                    entities.append(
                        create_entity(
                            name=function_name,
                            entity_type=entity_type,
                            language="python",
                            file_path=file_path,
                            start_line=node.start_point.row + 1,
                            end_line=node.end_point.row + 1,
                            metadata={
                                "parameters": parameters,
                                "class_name": current_class
                            }
                        )
                    )

            for child in node.named_children:
                traverse(child, current_class)

        traverse(tree.root_node)

        errors = []

        if tree.root_node.has_error:
            errors.append("Python contains syntax errors")

        return create_parse_result(
            language="python",
            entities=entities,
            errors=errors
        )