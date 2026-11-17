from backend.app.parsers.factory import ParserFactory

files = [
    "main.py",
    "server.js",
    "App.jsx"
]

for file in files:

    parser = ParserFactory.get_parser(file)

    print(file, "->", type(parser).__name__)