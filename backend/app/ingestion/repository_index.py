from collections import defaultdict


class RepositoryIndex:

    def build(self, scan_result: dict) -> dict:

        entities = scan_result.get("entities", [])
        relationships = scan_result.get("relationships", [])

        entities_by_name = defaultdict(list)
        entities_by_type = defaultdict(list)
        entities_by_language = defaultdict(list)
        entities_by_file = defaultdict(list)

        relationships_by_source = defaultdict(list)
        relationships_by_target = defaultdict(list)

        # Build entity indexes.
        for entity in entities:

            entities_by_name[entity["name"]].append(entity)

            entities_by_type[entity["type"]].append(entity)

            entities_by_language[entity["language"]].append(entity)

            file_path = entity.get("file_path")

            if file_path:
                entities_by_file[file_path].append(entity)

        # Build relationship indexes.
        for relationship in relationships:

            source = relationship["source"]
            target = relationship["target"]

            relationships_by_source[source].append(relationship)
            relationships_by_target[target].append(relationship)

        return {
            "repository_path": scan_result["repository_path"],

            "summary": {
                "files_discovered": scan_result["files_discovered"],
                "files_parsed": scan_result["files_parsed"],
                "total_entities": len(entities),
                "total_relationships": len(relationships)
            },

            "entities": entities,

            "relationships": relationships,

            "indexes": {
                "by_name": dict(entities_by_name),
                "by_type": dict(entities_by_type),
                "by_language": dict(entities_by_language),
                "by_file": dict(entities_by_file),
                "relationships_by_source": dict(relationships_by_source),
                "relationships_by_target": dict(relationships_by_target)
            },

            "errors": scan_result.get("errors", []),

            "files_skipped": scan_result.get("files_skipped", [])
        }