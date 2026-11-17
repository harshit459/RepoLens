from backend.app.parsers.factory import ParserFactory

samples = {
    "main.py": """
def calculate(a, b):
    return a + b
""",

    "app.js": """
function greet(name) {
    return "Hello " + name;
}
""",

    "index.html": """
<div class="container">
    <h1>Hello</h1>
    <button type="submit">Click</button>
</div>
""",

    "style.css": """
.container {
    display: flex;
    padding: 20px;
}

button {
    background-color: blue;
}
"""
}

for file_path, source_code in samples.items():

    parser = ParserFactory.get_parser(file_path)

    result = parser.parse(source_code, file_path=file_path)

    print(f"\n{'=' * 40}")
    print(f"FILE: {file_path}")
    print(f"{'=' * 40}")

    for entity in result["entities"]:
        print(entity)

    print("Errors:", result["errors"])