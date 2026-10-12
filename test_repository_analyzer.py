from backend.app.code_analysis.repository_analyzer import analyze_repository

repository_path = "."

definitions = analyze_repository(repository_path)

for definition in definitions:
    print(
    f"{definition['type'].capitalize()}: "
    f"{definition['name']} | "
    f"File: {definition['file']} | "
    f"Lines: {definition['start_line']}-{definition['end_line']}"
    )

print(f"\nTotal definitions found: {len(definitions)}")
