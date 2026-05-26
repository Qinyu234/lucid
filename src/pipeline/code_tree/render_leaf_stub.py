def render_leaf_stub(node: dict) -> str:
    from src.shared.format_io_comment import format_io_comment
    from src.shared.io_in_names import io_in_names
    from src.shared.io_out_names import io_out_names
    'Deterministic leaf skeleton that always passes verify_code.'
    fn = node.get('function_name') or 'module'
    io_in, io_out = format_io_comment(node.get('io'))
    semantic = node.get('semantic', '')
    lines = [f'# semantic: {semantic}', f'# io.in: {io_in}', f'# io.out: {io_out}', f'# skeleton: true', '', 'from src.shared.ctx_util import ctx_util', '', f'def {fn}(ctx):', '    ctx_util(ctx)', '    data = ctx.setdefault("data", {})']
    for key in io_in_names(node.get('io')):
        lines.append(f'    data.setdefault("{key}", None)  # read placeholder')
    for key in io_out_names(node.get('io')):
        lines.append(f'    data.setdefault("{key}", None)  # write placeholder')
    lines.append('    return ctx')
    lines.append('')
    return '\n'.join(lines)
