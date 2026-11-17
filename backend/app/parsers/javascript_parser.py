import tree_sitter_javascript as tsjavascript

from tree_sitter import Language, Parser
from .base import BaseParser

from .schema import create_entity, create_parse_result

class JavaScriptParser(BaseParser):

    def __init__(self):
        language = Language(tsjavascript.language())
        self.parser = Parser(language)

    def get_descendants(self, node):
        """Return all descendants of a node, including the node itself."""
        result = [node]

        for child in node.named_children:
            result.extend(self.get_descendants(child))

        return result


    def extract_props(self, params_node):
        """Extract basic props from destructured component parameters."""
        props = []
    
        if not params_node:
            return props
    
        # Handle: function UserCard({ name, age })
        first_param = (
            params_node.named_children[0]
            if params_node.named_children
            else None
        )
    
        if not first_param or first_param.type != "object_pattern":
            return props
    
        for child in first_param.named_children:
        
            if child.type == "shorthand_property_identifier_pattern":
                props.append(child.text.decode("utf8"))
    
            elif child.type == "pair_pattern":
                key_node = child.child_by_field_name("key")
    
                if key_node:
                    props.append(key_node.text.decode("utf8"))
    
        return props

    def extract_components(self, root_node):

        components = []

        nodes = self.get_descendants(root_node)

        for node in nodes:

            component_name = None
            params_node = None

            # Case 1: function UserCard() {}
            if node.type == "function_declaration":

                name_node = node.child_by_field_name("name")

                if name_node:
                    component_name = name_node.text.decode("utf8")

                params_node = node.child_by_field_name("parameters")

            # Case 2: const UserCard = () => {}
            elif node.type == "variable_declarator":

                name_node = node.child_by_field_name("name")
                value_node = node.child_by_field_name("value")

                if (
                    name_node
                    and value_node
                    and value_node.type in ("arrow_function", "function_expression")
                ):
                    component_name = name_node.text.decode("utf8")
                    params_node = value_node.child_by_field_name("parameters")

                    if params_node is None:
                        params_node = value_node.child_by_field_name("parameter")

                else:
                    continue

            else:
                continue

            # React components conventionally start with uppercase letters.
            if not component_name or not component_name[0].isupper():
                continue

            component_nodes = self.get_descendants(node)

            # A component must contain JSX.
            has_jsx = any(
                child.type in ("jsx_element", "jsx_self_closing_element")
                for child in component_nodes
            )

            if not has_jsx:
                continue

            props = self.extract_props(params_node)

            hooks = set()
            jsx_elements = set()

            for child in component_nodes:

                # Detect React hooks and custom hooks.
                if child.type == "call_expression":

                    function_node = child.child_by_field_name("function")

                    if function_node and function_node.type == "identifier":

                        function_name = function_node.text.decode("utf8")

                        if function_name.startswith("use"):
                            hooks.add(function_name)

                # Detect JSX tags.
                if child.type in (
                    "jsx_opening_element",
                    "jsx_self_closing_element"
                ):

                    name_node = child.child_by_field_name("name")

                    if name_node:
                        jsx_elements.add(name_node.text.decode("utf8"))

            components.append({
                "name": component_name,
                "props": props,
                "hooks": sorted(hooks),
                "jsx_elements": sorted(jsx_elements),
                "child_components": sorted(
                    element for element in jsx_elements
                    if element[0].isupper()
                )
            })

        return components

    def parse(self, source_code: str, file_path=None) -> dict:

        tree = self.parser.parse(source_code.encode("utf8"))
    
        entities = []
        relationships = []
    
        def traverse(node, current_class=None):
        
            if node.type == "class_declaration":
                name_node = node.child_by_field_name("name")
    
                current_class = (
                    name_node.text.decode("utf8")
                    if name_node else None
                )
    
                if current_class:
                    entities.append(
                        create_entity(
                            name=current_class,
                            entity_type="class",
                            language="javascript",
                            start_line=node.start_point.row + 1,
                            end_line=node.end_point.row + 1,
                            file_path=file_path
                        )
                    )
    
            if node.type in ("function_declaration", "method_definition"):
            
                name_node = node.child_by_field_name("name")
                params_node = node.child_by_field_name("parameters")
    
                if name_node:
                    parameters = []
    
                    if params_node:
                        parameters = [
                            param.text.decode("utf8")
                            for param in params_node.named_children
                        ]
    
                    function_name = name_node.text.decode("utf8")
    
                    entities.append(
                        create_entity(
                            name=function_name,
                            entity_type=(
                                "method"
                                if node.type == "method_definition"
                                else "function"
                            ),
                            language="javascript",
                            start_line=node.start_point.row + 1,
                            end_line=node.end_point.row + 1,
                            file_path=file_path,
                            metadata={
                                "parameters": parameters,
                                "class_name": current_class
                            }
                        )
                    )
    
            if node.type == "variable_declarator":
            
                name_node = node.child_by_field_name("name")
                value_node = node.child_by_field_name("value")
    
                if (
                    name_node
                    and value_node
                    and value_node.type == "arrow_function"
                ):
    
                    function_name = name_node.text.decode("utf8")
    
                    params_node = (
                        value_node.child_by_field_name("parameters")
                        or value_node.child_by_field_name("parameter")
                    )
    
                    parameters = []
    
                    if params_node:
                        if params_node.type == "formal_parameters":
                            parameters = [
                                param.text.decode("utf8")
                                for param in params_node.named_children
                            ]
                        else:
                            parameters = [params_node.text.decode("utf8")]
    
                    entities.append(
                        create_entity(
                            name=function_name,
                            entity_type="arrow_function",
                            language="javascript",
                            start_line=node.start_point.row + 1,
                            end_line=node.end_point.row + 1,
                            file_path=file_path,
                            metadata={
                                "parameters": parameters,
                                "class_name": current_class
                            }
                        )
                    )
    
            for child in node.named_children:
                traverse(child, current_class)
    
        traverse(tree.root_node)
    
        # Extract React components separately.
        components = self.extract_components(tree.root_node)
    
        for component in components:

            component_node = next(
                (
                    node for node in self.get_descendants(tree.root_node)
                    if (
                        node.type == "function_declaration"
                        and node.child_by_field_name("name")
                        and node.child_by_field_name("name").text.decode("utf8")
                        == component["name"]
                    )
                    or (
                        node.type == "variable_declarator"
                        and node.child_by_field_name("name")
                        and node.child_by_field_name("name").text.decode("utf8")
                        == component["name"]
                    )
                ),
                None
            )
        
            if component_node is None:
                continue
            
            start_line = component_node.start_point.row + 1
            end_line = component_node.end_point.row + 1
        
            component_entity = next(
                (
                    entity for entity in entities
                    if entity["name"] == component["name"]
                    and entity["start_line"] == start_line
                    and entity["end_line"] == end_line
                ),
                None
            )
        
            component_metadata = {
                "props": component["props"],
                "hooks": component["hooks"],
                "jsx_elements": component["jsx_elements"],
                "child_components": component.get("child_components", [])
            }
        
            if component_entity:
                component_entity["type"] = "component"
                component_entity["metadata"].update(component_metadata)
        
            else:
                entities.append(
                    create_entity(
                        name=component["name"],
                        entity_type="component",
                        language="javascript",
                        start_line=start_line,
                        end_line=end_line,
                        file_path=file_path,
                        metadata=component_metadata
                    )
                )
        
            for child_component in component.get("child_components", []):
                relationships.append({
                    "source": component["name"],
                    "target": child_component,
                    "type": "renders"
                })
    
        return create_parse_result(
            language="javascript",
            entities=entities,
            relationships=relationships
        )