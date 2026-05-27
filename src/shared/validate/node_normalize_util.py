def node_normalize_util(node: dict) -> dict:
    from src.shared.validate.io_empty_util import io_empty_util
    from src.shared.validate.io_normalize_util import io_normalize_util
    if 'io' in node:
        node['io'] = io_normalize_util(node['io'])
        return node
    if 'input' in node or 'output' in node:
        inp = node.pop('input', {})
        out = node.pop('output', {})
        node['io'] = io_normalize_util({'in': inp.get('data_keys', []) if isinstance(inp, dict) else [], 'out': out.get('data_keys', []) if isinstance(out, dict) else []})
        return node
    node['io'] = io_empty_util()
    return node
