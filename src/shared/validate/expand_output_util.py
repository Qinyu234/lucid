def expand_output_util(data: dict):
    from src.shared.lib.schema_util import schema_util
    from src.shared.validate.schema_util import schema_util
    schema = schema_util('expand_schema.json')
    return schema_util(data, schema)
