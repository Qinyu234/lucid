def repair_seq_io_chain(children: list) -> list:
    from src.shared.normalize_io import normalize_io
    '\n    For SEQ siblings, add missing upstream.out keys required by downstream.in.\n    Returns human-readable repair notes (empty if nothing changed).\n    '
    notes = []
    if len(children) < 2:
        return notes
    for i in range(len(children) - 1):
        left = children[i]
        right = children[i + 1]
        left_io = normalize_io(left.get('io'))
        right_io = normalize_io(right.get('io'))
        out_names = {f.get('name') for f in left_io.get('out', []) if f.get('name')}
        changed = False
        for inf in right_io.get('in', []):
            name = inf.get('name')
            if not name or name in out_names:
                continue
            left_io.setdefault('out', []).append({'name': name, 'type': inf.get('type') or 'any'})
            out_names.add(name)
            changed = True
            notes.append(f"step[{i}]->step[{i + 1}]: added upstream.out '{name}'")
        if changed:
            left['io'] = left_io
    return notes
