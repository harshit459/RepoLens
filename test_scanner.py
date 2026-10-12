from backend.app.ingestion.repository_scanner import scan_python_files

files = scan_python_files(".")

for file_path in files:
    print(file_path)

print(f"\nTotal Python files found: {len(files)}")
