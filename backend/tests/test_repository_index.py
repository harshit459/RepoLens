import unittest

from backend.app.ingestion.repository_index import RepositoryIndex


class TestRepositoryIndex(unittest.TestCase):

    def test_build_repository_index(self):

        scan_result = {
            "repository_path": "sample-project",

            "files_discovered": 3,
            "files_parsed": 3,

            "entities": [
                {
                    "name": "calculate",
                    "type": "function",
                    "language": "python",
                    "file_path": "calculator.py",
                    "start_line": 1,
                    "end_line": 3,
                    "metadata": {}
                },
                {
                    "name": "calculate",
                    "type": "function",
                    "language": "python",
                    "file_path": "statistics.py",
                    "start_line": 5,
                    "end_line": 8,
                    "metadata": {}
                },
                {
                    "name": "App",
                    "type": "component",
                    "language": "javascript",
                    "file_path": "App.jsx",
                    "start_line": 1,
                    "end_line": 10,
                    "metadata": {}
                }
            ],

            "relationships": [],

            "errors": [],
            "files_skipped": []
        }

        indexer = RepositoryIndex()

        index = indexer.build(scan_result)

        # Check summary.
        self.assertEqual(
            index["summary"]["total_entities"], 3
        )

        # Check duplicate names.
        calculate_entities = (
            index["indexes"]["by_name"]["calculate"]
        )

        self.assertEqual(len(calculate_entities), 2)

        # Check language index.
        python_entities = (
            index["indexes"]["by_language"]["python"]
        )

        self.assertEqual(len(python_entities), 2)

        # Check file index.
        calculator_entities = (
            index["indexes"]["by_file"]["calculator.py"]
        )

        self.assertEqual(len(calculator_entities), 1)

        # Check type index.
        components = (
            index["indexes"]["by_type"]["component"]
        )

        self.assertEqual(len(components), 1)


if __name__ == "__main__":
    unittest.main()