import tree_sitter_html as tshtml

from tree_sitter import Language, Parser
from .base import BaseParser
from .schema import create_entity, create_parse_result


class HTMLParser(BaseParser):

    def __init__(self):
        language = Language(tshtml.language())
        self.parser = Parser(language)

    def parse(self, source_code: str, file_path=None) -> dict:

        tree = self.parser.parse(source_code.encode("utf8"))

        entities = []

        def traverse(node):

            if node.type in ("start_tag", "self_closing_tag"):

                name_node = next(
                    (
                        child for child in node.named_children
                        if child.type == "tag_name"
                    ),
                    None
                )

                if name_node:

                    tag_name = name_node.text.decode("utf8")
                    attributes = {}

                    for child in node.named_children:

                        if child.type == "attribute":

                            attribute_name = next(
                                (node for node in child.named_children
                                 if node.type == "attribute_name"),
                                None
                            )

                            attribute_value = next(
                                (
                                    descendant
                                    for node in child.named_children
                                    for descendant in node.named_children
                                    if descendant.type == "attribute_value"
                                ),
                                None
                            )

                            if attribute_name:
                                attributes[
                                    attribute_name.text.decode("utf8")
                                ] = (
                                    attribute_value.text.decode("utf8")
                                    if attribute_value else True
                                )

                    entities.append(
                        create_entity(
                            name=tag_name,
                            entity_type="html_element",
                            language="html",
                            start_line=node.start_point.row + 1,
                            end_line=node.end_point.row + 1,
                            file_path=file_path,
                            metadata={
                                "attributes": attributes
                            }
                        )
                    )

            for child in node.named_children:
                traverse(child)

        traverse(tree.root_node)

        errors = []

        if tree.root_node.has_error:
            errors.append("HTML contains syntax errors")

        return create_parse_result(
            language="html",
            entities=entities,
            errors=errors
        )