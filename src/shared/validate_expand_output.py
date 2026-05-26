def validate_expand_output(data: dict):
    from src.shared.load_schema import load_schema
    from src.shared.validate import validate
    schema = load_schema('expand_schema.json')
    return validate(data, schema)
