from src.schema.engine import load_schema, validate


def validate_job_input(data: dict):
    schema = load_schema("data_schema.json")
    return validate(data, schema)
