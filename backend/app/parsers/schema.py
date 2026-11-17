def create_entity(
    name: str,
    entity_type: str,
    language: str,
    start_line: int,
    end_line: int,
    metadata: dict = None,
    file_path: str = None
) -> dict:

    return {
        "name": name,
        "type": entity_type,
        "language": language,
        "file_path": file_path,
        "start_line": start_line,
        "end_line": end_line,
        "metadata": metadata or {}
    }


def create_parse_result(
    language: str,
    entities: list = None,
    relationships: list = None,
    errors: list = None
) -> dict:

    return {
        "language": language,
        "entities": entities or [],
        "relationships": relationships or [],
        "errors": errors or []
    }