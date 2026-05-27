def job_input_util(data: dict):
    from src.shared.lib.schema_util import schema_util as load_schema_util
    from src.shared.validate.schema_util import schema_util as validate_schema_util

    schema = load_schema_util("data_schema.json")
    return validate_schema_util(data, schema)
