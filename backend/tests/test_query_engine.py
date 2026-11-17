import unittest

from backend.app.ingestion.query_engine import RepositoryQueryEngine


class TestRepositoryQueryEngine(unittest.TestCase):

    def setUp(self):

        self.repository_index = {
            "repository_path": "sample-project",

            "summary": {
                "files_discovered": 3,
                "files_parsed": 3,
                "total_entities": 4,
                "total_relationships": 1
            },

            "entities": [
                {
                    "name": "calculate",
                    "type": "function",
                    "language": "python",
                    "file_path": "calculator.py",
                    "metadata": {}
                },
                {
                    "name": "multiply",
                    "type": "function",
                    "language": "python",
                    "file_path": "calculator.py",
                    "metadata": {}
                },
                {
                    "name": "calculate",
                    "type": "function",
                    "language": "javascript",
                    "file_path": "calculator.js",
                    "metadata": {}
                },
                {
                    "name": "App",
                    "type": "component",
                    "language": "javascript",
                    "file_path": "App.jsx",
                    "metadata": {}
                }
            ],

            "relationships": [
                {
                    "source": "App",
                    "target": "UserCard",
                    "type": "renders"
                }
            ],

            "indexes": {
                "by_name": {
                    "calculate": [],
                    "multiply": [],
                    "App": []
                },

                "by_type": {
                    "function": [],
                    "component": []
                },

                "by_language": {
                    "python": [],
                    "javascript": []
                },

                "by_file": {
                    "calculator.py": [],
                    "calculator.js": [],
                    "App.jsx": []
                },

                "relationships_by_source": {
                    "App": [
                        {
                            "source": "App",
                            "target": "UserCard",
                            "type": "renders"
                        }
                    ]
                },

                "relationships_by_target": {
                    "UserCard": [
                        {
                            "source": "App",
                            "target": "UserCard",
                            "type": "renders"
                        }
                    ]
                }
            }
        }

        # Populate the indexes from the entities.
        for entity in self.repository_index["entities"]:

            self.repository_index["indexes"]["by_name"].setdefault(
                entity["name"], []
            ).append(entity)

            self.repository_index["indexes"]["by_type"].setdefault(
                entity["type"], []
            ).append(entity)

            self.repository_index["indexes"]["by_language"].setdefault(
                entity["language"], []
            ).append(entity)

            self.repository_index["indexes"]["by_file"].setdefault(
                entity["file_path"], []
            ).append(entity)

        self.engine = RepositoryQueryEngine(
            self.repository_index
        )

    def test_search_by_name(self):
        result = self.engine.search_by_name("calculate")
        self.assertEqual(len(result), 2)

    def test_search_by_type(self):
        result = self.engine.search_by_type("component")
        self.assertEqual(len(result), 1)

    def test_search_by_language(self):
        result = self.engine.search_by_language("python")
        self.assertEqual(len(result), 2)

    def test_search_by_file(self):
        result = self.engine.search_by_file("calculator.py")
        self.assertEqual(len(result), 2)

    def test_partial_name_search(self):
        result = self.engine.search_name_contains("calc")
        self.assertEqual(len(result), 2)

    def test_relationship_search(self):
        result = self.engine.get_relationships("App")

        self.assertEqual(len(result["outgoing"]), 1)
        self.assertEqual(len(result["incoming"]), 0)

    def test_summary(self):
        result = self.engine.get_summary()

        self.assertEqual(result["total_entities"], 4)


if __name__ == "__main__":
    unittest.main()