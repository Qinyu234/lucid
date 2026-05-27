def node_schema_util(node: dict, strict: bool=False):
    from copy import deepcopy
    from src.shared.lib.schema_util import schema_util
    from src.shared.validate.schema_util import schema_util
    from src.shared.validate.io_normalize_util import io_normalize_util
    from src.shared.validate.node_normalize_util import node_normalize_util
    prepared = node_normalize_util(deepcopy(node))
    prepared.setdefault('children', [])
    prepared.setdefault('code_path', '')
    schema = schema_util('node_schema.json')
    result = schema_util(prepared, schema)
    if strict and prepared.get('status') == 'growing' and prepared.get('children'):
        result.fail('$.children: growing node must not have children yet')
    return (result, prepared)
