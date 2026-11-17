from backend.app.parsers.schema import (
    create_entity,
    create_parse_result
)

entity = create_entity(
    name="UserCard",
    entity_type="component",
    language="javascript",
    start_line=1,
    end_line=10,
    metadata={"props": ["name", "age"]}
)

result = create_parse_result(
    language="javascript",
    entities=[entity]
)

print(result)