from .emit_flow import emit_flow

def render_init(node: dict) -> str:
    from src.shared.format_io_comment import format_io_comment

    def _import_child(fn: str) -> str:
        return f'from .{fn} import {fn}'

    def _file_header(node: dict) -> str:
        io_in, io_out = format_io_comment(node.get('io'))
        return f"# semantic: {node.get('semantic', '')}\n# io.in: {io_in}\n# io.out: {io_out}\n# topology: {node.get('topology') or 'SEQ'}\n\n"
    children = node.get('children', [])
    topology = node.get('topology') or 'SEQ'
    header = _file_header(node)
    pkg = node.get('function_name') or 'package'
    if not children:
        return header + f'def {pkg}(ctx):\n    return ctx\n'
    lines = [header]
    for child in children:
        lines.append(f"{_import_child(child['function_name'])}\n")
    lines.append(f'\ndef {pkg}(ctx):\n')
    lines.extend((f'{line}\n' for line in emit_flow(children, topology)))
    return ''.join(lines)
