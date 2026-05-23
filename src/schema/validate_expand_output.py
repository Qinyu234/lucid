from src.schema.engine import load_schema, validate


def validate_expand_output(data: dict):
    schema = load_schema("expand_schema.json")
    return validate(data, schema)
