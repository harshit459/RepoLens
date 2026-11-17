import unittest

from pathlib import Path
from tempfile import TemporaryDirectory

from backend.app.ingestion.repository_scanner import RepositoryScanner


class TestRepositoryScanner(unittest.TestCase):

    def test_repository_scanning(self):

        with TemporaryDirectory() as temp_dir:

            root = Path(temp_dir)

            # Create sample source files.
            (root / "main.py").write_text(
                "def calculate(a, b):\n    return a + b",
                encoding="utf-8"
            )

            (root / "app.js").write_text(
                "function greet(name) { return name; }",
                encoding="utf-8"
            )

            (root / "index.html").write_text(
                '<div class="container"></div>',
                encoding="utf-8"
            )

            (root / "style.css").write_text(
                ".container { display: flex; }",
                encoding="utf-8"
            )

            # Unsupported file.
            (root / "README.md").write_text(
                "# Test Project",
                encoding="utf-8"
            )

            # Ignored directory.
            ignored_dir = root / "node_modules"
            ignored_dir.mkdir()

            (ignored_dir / "ignored.js").write_text(
                "function ignored() {}",
                encoding="utf-8"
            )

            scanner = RepositoryScanner()

            result = scanner.scan(str(root))

            self.assertEqual(result["files_discovered"], 5)
            self.assertEqual(result["files_parsed"], 4)

            self.assertGreater(len(result["entities"]), 0)

            languages = {
                entity["language"]
                for entity in result["entities"]
            }

            self.assertEqual(
                languages,
                {"python", "javascript", "html", "css"}
            )

            skipped_paths = [
                file["file_path"]
                for file in result["files_skipped"]
            ]

            self.assertIn("README.md", skipped_paths)

            self.assertEqual(result["errors"], [])


if __name__ == "__main__":
    unittest.main()