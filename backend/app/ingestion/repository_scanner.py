import os
import tokenize

from pathlib import Path

from ..parsers.factory import ParserFactory


class RepositoryScanner:

    IGNORED_DIRS = {
        ".git",
        ".venv",
        "venv",
        "env",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".idea",
        ".vscode",
        "dist",
        "build",
        ".next",
    }

    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB

    def scan(self, repository_path: str) -> dict:

        root = Path(repository_path).resolve()

        if not root.exists() or not root.is_dir():
            raise ValueError(
                f"Invalid repository directory: {repository_path}"
            )

        entities = []
        relationships = []

        files_discovered = 0
        files_parsed = 0

        skipped_files = []
        errors = []

        for current_root, directories, files in os.walk(root):

            # Prevent traversal into ignored directories.
            directories[:] = [
                directory
                for directory in directories
                if directory not in self.IGNORED_DIRS
            ]

            for filename in files:

                file_path = Path(current_root) / filename

                relative_path = file_path.relative_to(root).as_posix()

                files_discovered += 1

                # Select the correct parser.
                parser = ParserFactory.get_parser(str(file_path))

                if parser is None:
                    skipped_files.append({
                        "file_path": relative_path,
                        "reason": "Unsupported file extension"
                    })
                    continue

                try:

                    # Skip unusually large files.
                    if file_path.stat().st_size > self.MAX_FILE_SIZE:
                        skipped_files.append({
                            "file_path": relative_path,
                            "reason": "File exceeds size limit"
                        })
                        continue

                    # Python source files can declare their encoding.
                    if file_path.suffix.lower() == ".py":
                        with tokenize.open(file_path) as file:
                            source_code = file.read()
                    else:
                        source_code = file_path.read_text(
                            encoding="utf-8-sig"
                        )

                    # Parse the source code.
                    result = parser.parse(
                        source_code,
                        file_path=relative_path
                    )

                    files_parsed += 1

                    entities.extend(result["entities"])
                    relationships.extend(result["relationships"])

                    for error in result["errors"]:
                        errors.append({
                            "file_path": relative_path,
                            "message": error
                        })

                except Exception as error:
                    errors.append({
                        "file_path": relative_path,
                        "message": str(error)
                    })

        return {
            "repository_path": str(root),
            "files_discovered": files_discovered,
            "files_parsed": files_parsed,
            "files_skipped": skipped_files,
            "entities": entities,
            "relationships": relationships,
            "errors": errors
        }