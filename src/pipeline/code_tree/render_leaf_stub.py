def render_leaf_stub(node: dict) -> str:
    from src.shared.validate.io_format_comment_util import io_format_comment_util
    from src.shared.validate.io_in_names_util import io_in_names_util
    from src.shared.validate.io_out_names_util import io_out_names_util
    'Deterministic leaf skeleton that always passes verify_code.'
    fn = node.get('function_name') or 'module'
    io_in, io_out = io_format_comment_util(node.get('io'))
    semantic = node.get('semantic', '')
    lines = [f'# semantic: {semantic}', f'# io.in: {io_in}', f'# io.out: {io_out}', f'# skeleton: true', '', f'def {fn}(ctx):', '    ctx.setdefault("data", {})', '    ctx.setdefault("meta", {})', '    ctx.setdefault("state", {})', '    ctx.setdefault("error", None)', '    data = ctx["data"]']
    for key in io_in_names_util(node.get('io')):
        lines.append(f'    data.setdefault("{key}", None)  # read placeholder')
    for key in io_out_names_util(node.get('io')):
        lines.append(f'    data.setdefault("{key}", None)  # write placeholder')
    lines.append('    return ctx')
    lines.append('')
    return '\n'.join(lines)
