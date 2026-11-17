import tree_sitter_css as tscss

from tree_sitter import Language, Parser
from .base import BaseParser
from .schema import create_entity, create_parse_result


class CSSParser(BaseParser):

    def __init__(self):
        language = Language(tscss.language())
        self.parser = Parser(language)

    def parse(self, source_code: str, file_path=None) -> dict:

        tree = self.parser.parse(source_code.encode("utf8"))

        entities = []

        def traverse(node):

            if node.type == "rule_set":

                selectors_node = next(
                    (child for child in node.named_children
                     if child.type == "selectors"),
                    None
                )
            
                block_node = next(
                    (child for child in node.named_children
                     if child.type == "block"),
                    None
                )
            
                if selectors_node:
                
                    selector_names = [
                        child.text.decode("utf8")
                        for child in selectors_node.named_children
                    ]
            
                    declarations = []
            
                    if block_node:
                        for child in block_node.named_children:
                        
                            if child.type == "declaration":
                            
                                property_node = next(
                                    (n for n in child.named_children
                                     if n.type == "property_name"),
                                    None
                                )
            
                                value_node = next(
                                    (n for n in child.named_children
                                     if n.type != "property_name"),
                                    None
                                )
            
                                if property_node:
                                    declarations.append({
                                        "property": property_node.text.decode("utf8"),
                                        "value": (
                                            value_node.text.decode("utf8")
                                            if value_node else None
                                        )
                                    })
            
                    entities.append(
                        create_entity(
                            name=", ".join(selector_names),
                            entity_type="css_rule",
                            language="css",
                            start_line=node.start_point.row + 1,
                            end_line=node.end_point.row + 1,
                            file_path=file_path,
                            metadata={
                                "selectors": selector_names,
                                "declarations": declarations
                            }
                        )
                    )
            
            for child in node.named_children:
                traverse(child)

        traverse(tree.root_node)

        errors = []

        if tree.root_node.has_error:
            errors.append("CSS contains syntax errors")

        return create_parse_result(
            language="css",
            entities=entities,
            errors=errors
        )