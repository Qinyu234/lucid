def register_tree_io(root: dict, job: dict | None=None, parent: dict | None=None, registry: dict | None=None):
    from src.shared.normalize_io import normalize_io

    def _merge_module(registry: dict, node: dict, parent: dict | None):
        fn = node.get('function_name') or 'unnamed'
        io = normalize_io(node.get('io'))
        parent_fn = (parent or {}).get('function_name')
        registry['modules'][fn] = {'semantic': node.get('semantic', ''), 'io': io, 'parent': parent_fn, 'topology': node.get('topology'), 'code_path': node.get('code_path')}
        used_by = []
        if parent_fn:
            used_by.append({'module': parent_fn, 'import': f'from .{fn} import {fn}', 'location': f"{parent.get('code_path', '')}/__init__.py"})
        for side in ('in', 'out'):
            for field in io.get(side, []):
                name = field['name']
                entry = registry['fields'].setdefault(name, {'type': field['type'], 'produced_by': [], 'consumed_by': []})
                if entry.get('type') and entry['type'] != field['type'] and (field['type'] != 'any'):
                    entry['type_conflict'] = entry.get('type', field['type'])
                if field['type'] != 'any':
                    entry['type'] = field['type']
                ref = {'module': fn, 'side': side}
                if side == 'in':
                    if ref not in entry['consumed_by']:
                        entry['consumed_by'].append(ref)
                elif ref not in entry['produced_by']:
                    entry['produced_by'].append(ref)
                if used_by and side == 'out':
                    entry.setdefault('used_by', [])
                    for u in used_by:
                        if u not in entry['used_by']:
                            entry['used_by'].append(u)
    if registry is None:
        registry = {'fields': {}, 'modules': {}}
    _merge_module(registry, root, parent)
    for child in root.get('children', []):
        register_tree_io(child, job, parent=root, registry=registry)
    return registry
