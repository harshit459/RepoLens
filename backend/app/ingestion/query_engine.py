class RepositoryQueryEngine:

    def __init__(self, repository_index: dict):
        self.index = repository_index
        self.indexes = repository_index["indexes"]

    def search_by_name(self, name: str) -> list:
        """
        Find entities with an exact name.
        """
        return self.indexes["by_name"].get(name, [])

    def search_by_type(self, entity_type: str) -> list:
        """
        Find entities by type.
        Example: function, class, component, css_rule.
        """
        return self.indexes["by_type"].get(entity_type, [])

    def search_by_language(self, language: str) -> list:
        """
        Find entities belonging to a programming language.
        """
        return self.indexes["by_language"].get(language.lower(), [])

    def search_by_file(self, file_path: str) -> list:
        """
        Find all entities extracted from a particular file.
        """
        normalized_path = file_path.replace("\\", "/")

        return self.indexes["by_file"].get(normalized_path, [])

    def search_name_contains(self, query: str) -> list:
        """
        Find entities whose names contain the given text.
        """
        query = query.lower()

        return [
            entity
            for entity in self.index["entities"]
            if query in entity["name"].lower()
        ]

    def get_relationships(self, entity_name: str) -> dict:
        """
        Find incoming and outgoing relationships.
        """
        return {
            "outgoing": self.indexes[
                "relationships_by_source"
            ].get(entity_name, []),

            "incoming": self.indexes[
                "relationships_by_target"
            ].get(entity_name, [])
        }

    def get_summary(self) -> dict:
        """
        Return repository-level statistics.
        """
        return self.index["summary"]