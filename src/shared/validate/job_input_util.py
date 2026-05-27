def job_input_util(data: dict):
    from src.shared.lib.schema_util import schema_util
    from src.shared.validate.schema_util import schema_util
    schema = schema_util('data_schema.json')
    return schema_util(data, schema)
