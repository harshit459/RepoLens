from backend.app.ingestion.repository_scanner import scan_python_files
from backend.app.code_analysis.python_analyzer import analyze_python_file

def analyze_repository(repository_path):
    python_files = scan_python_files(repository_path)
    all_definitions = []

    for file_path in python_files:
        try:
            definitions = analyze_python_file(file_path)
            all_definitions.extend(definitions)

        except (SyntaxError, UnicodeDecodeError) as error:
            print(f"Skipping {file_path}: {error}")

    return all_definitions
