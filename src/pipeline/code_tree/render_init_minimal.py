def render_init_minimal(node: dict) -> str:
    from src.shared.format_io_comment import format_io_comment
    'Fallback composite skeleton when full render_init fails verify.'
    children = node.get('children', [])
    pkg = node.get('function_name') or 'package'
    io_in, io_out = format_io_comment(node.get('io'))
    topology = node.get('topology') or 'SEQ'
    lines = [f"# semantic: {node.get('semantic', '')}", f'# io.in: {io_in}', f'# io.out: {io_out}', f'# topology: {topology}', f'# skeleton: true', '']
    for child in children:
        fn = child['function_name']
        lines.append(f'from .{fn} import {fn}')
    lines.append('')
    lines.append(f'def {pkg}(ctx):')
    lines.append('    ctx.setdefault("data", {})')
    lines.append('    ctx.setdefault("meta", {})')
    lines.append('    ctx.setdefault("state", {})')
    lines.append('    ctx.setdefault("error", None)')
    if topology == 'ROUTER' and children:
        default = children[0]['function_name']
        lines.append('    case = ctx.get("meta", {}).get("case")')
        lines.append('    if case is None:')
        lines.append(f'        return {default}(ctx)')
        for i, child in enumerate(children):
            fn = child['function_name']
            case_id = child.get('case') or f'CASE_{i}'
            lines.append(f'    if case == "{case_id}":')
            lines.append(f'        return {fn}(ctx)')
        lines.append(f'    return {default}(ctx)')
    else:
        for child in children:
            fn = child['function_name']
            lines.append(f'    ctx = {fn}(ctx)')
        lines.append('    return ctx')
    lines.append('')
    return '\n'.join(lines)
