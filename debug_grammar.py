import tree_sitter_html as tshtml
import tree_sitter_css as tscss

from tree_sitter import Language, Parser


html_parser = Parser(Language(tshtml.language()))

html_code = """
<div class="container">
    <h1>Hello</h1>
    <button type="submit">Click</button>
</div>
"""

html_tree = html_parser.parse(html_code.encode("utf8"))

print("========== HTML TREE ==========")
print(html_tree.root_node)


css_parser = Parser(Language(tscss.language()))

css_code = """
.container {
    display: flex;
    padding: 20px;
}

button {
    background-color: blue;
}
"""

css_tree = css_parser.parse(css_code.encode("utf8"))

print("\n========== CSS TREE ==========")
print(css_tree.root_node)

print("\n========== CSS NODE DETAILS ==========")

def inspect(node, depth=0):
    indent = "  " * depth

    print(
        indent,
        "TYPE:", node.type,
        "| TEXT:", node.text.decode("utf8")[:60]
    )

    if node.type == "rule_set":
        print("Selectors field:", node.child_by_field_name("selectors"))
        print("Block field:", node.child_by_field_name("block"))

    if node.type == "declaration":
        print("Property field:", node.child_by_field_name("property"))
        print("Value field:", node.child_by_field_name("value"))

    for child in node.named_children:
        inspect(child, depth + 1)


inspect(css_tree.root_node)