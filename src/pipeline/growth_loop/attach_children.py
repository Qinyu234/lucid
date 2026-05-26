def attach_children(node, proposal, topology: str, boundary: dict | None=None):
    from src.shared.merge_io_router import merge_io_router
    from src.shared.merge_io_seq import merge_io_seq
    from src.shared.normalize_io import normalize_io
    from src.pipeline.child_code_path import child_code_path
    from src.pipeline.growth_loop.dedupe_sibling_names import dedupe_sibling_names
    if not proposal:
        return
    node['topology'] = topology
    node.setdefault('children', [])
    parent_path = (node.get('code_path') or '').rstrip('/\\')
    parent_depth = node.get('depth', 0)
    for p in proposal:
        fn = p.get('function_name') or 'unnamed'
        child = {'semantic': p.get('semantic', ''), 'function_name': fn, 'children': [], 'status': 'growing', 'role': 'leaf', 'code_path': child_code_path(parent_path, fn), 'depth': parent_depth + 1, 'topology': None, 'tag': p.get('tag'), 'case': p.get('case'), 'io': normalize_io(p.get('io')), 'code_ok': None}
        node['children'].append(child)
    dedupe_sibling_names(node['children'])
    for child in node['children']:
        child['code_path'] = child_code_path(parent_path, child['function_name'])
    if topology == 'ROUTER':
        for i, child in enumerate(node['children']):
            if not child.get('case'):
                child['case'] = f'CASE_{i}'
            if not child.get('tag'):
                child['tag'] = child.get('case')
    merged = merge_io_router(node['children']) if topology == 'ROUTER' else merge_io_seq(node['children'])
    if boundary and boundary.get('io'):
        bio = normalize_io(boundary['io'])
        if bio['in']:
            merged['in'] = bio['in']
        if bio['out']:
            merged['out'] = bio['out']
    node['io'] = merged
