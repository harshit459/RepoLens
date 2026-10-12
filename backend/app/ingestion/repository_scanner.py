from pathlib import Path

IGNORED_DIRECTORIES = {
".git",
".venv",
"venv",
"**pycache**",
"node_modules",
".pytest_cache",
".mypy_cache",
}

def scan_python_files(repository_path):
    root = Path(repository_path).resolve()

    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    python_files = []

    for current_path in root.rglob("*.py"):
        relative_path = current_path.relative_to(root)

        if any(
            part in IGNORED_DIRECTORIES
            for part in relative_path.parts[:-1]
        ):
            continue

        if current_path.is_file():
            python_files.append(current_path)

    return sorted(python_files)
