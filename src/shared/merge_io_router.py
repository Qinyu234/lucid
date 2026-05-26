def merge_io_router(children: list) -> dict:
    from src.shared.empty_io import empty_io
    from src.shared.normalize_io import normalize_io
    if not children:
        return empty_io()
    in_map = {}
    out_map = {}
    for child in children:
        for f in normalize_io(child.get('io')).get('in', []):
            in_map.setdefault(f['name'], f['type'])
        for f in normalize_io(child.get('io')).get('out', []):
            out_map.setdefault(f['name'], f['type'])
    return {'in': [{'name': k, 'type': v} for k, v in sorted(in_map.items())], 'out': [{'name': k, 'type': v} for k, v in sorted(out_map.items())]}
