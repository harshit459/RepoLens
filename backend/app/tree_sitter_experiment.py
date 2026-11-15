import tree_sitter_python as tspython
from tree_sitter import Language, Parser

# Load Python grammar
PY_LANGUAGE = Language(tspython.language())

# Create parser
parser = Parser(PY_LANGUAGE)


def extract_metadata(node):
    metadata = {
        "functions": [],
        "classes": []
    }

    def traverse(current_node, current_class=None):

        if current_node.type == "class_definition":
            name_node = current_node.child_by_field_name("name")
            class_name = name_node.text.decode("utf8")

            metadata["classes"].append({
                "name": class_name,
                "start_line": current_node.start_point.row + 1,
                "end_line": current_node.end_point.row + 1
            })

            current_class = class_name

        if current_node.type == "function_definition":

            name_node = current_node.child_by_field_name("name")
            params_node = current_node.child_by_field_name("parameters")

            parameters = []

            if params_node:
                for param in params_node.named_children:
                    parameters.append(param.text.decode("utf8"))

            metadata["functions"].append({
                "name": name_node.text.decode("utf8"),
                "type": "method" if current_class else "function",
                "class_name": current_class,
                "parameters": parameters,
                "start_line": current_node.start_point.row + 1,
                "end_line": current_node.end_point.row + 1
            })

        for child in current_node.named_children:
            traverse(child, current_class)

    traverse(node)

    return metadata


code = """
def authenticate(username, password):
    return True

class PaymentService:

    def process_payment(self, amount):
        return amount * 0.9

    def refund_payment(self, transaction_id):
        return True
"""

tree = parser.parse(code.encode("utf8"))

result = extract_metadata(tree.root_node)

print(result)