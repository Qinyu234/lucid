def io_merge_router_util(children: list) -> dict:
    from src.shared.validate.io_empty_util import io_empty_util
    from src.shared.validate.io_normalize_util import io_normalize_util
    if not children:
        return io_empty_util()
    in_map = {}
    out_map = {}
    for child in children:
        for f in io_normalize_util(child.get('io')).get('in', []):
            in_map.setdefault(f['name'], f['type'])
        for f in io_normalize_util(child.get('io')).get('out', []):
            out_map.setdefault(f['name'], f['type'])
    return {'in': [{'name': k, 'type': v} for k, v in sorted(in_map.items())], 'out': [{'name': k, 'type': v} for k, v in sorted(out_map.items())]}
