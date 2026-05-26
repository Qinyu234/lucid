def validate_job_input(data: dict):
    from src.shared.load_schema import load_schema
    from src.shared.validate import validate
    schema = load_schema('data_schema.json')
    return validate(data, schema)
