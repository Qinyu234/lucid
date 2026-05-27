from .emit_flow import emit_flow
from .format_io_bridge import format_io_bridge


def render_init(node: dict) -> str:
    def _import_child(fn: str) -> str:
        return f"from .{fn} import {fn}"

    def _file_header(node: dict) -> str:
        io_in, io_out = format_io_bridge(node.get("io"))
        return (
            f"# semantic: {node.get('semantic', '')}\n"
            f"# io.in: {io_in}\n"
            f"# io.out: {io_out}\n"
            f"# topology: {node.get('topology') or 'SEQ'}\n\n"
        )

    children = node.get("children", [])
    topology = node.get("topology") or "SEQ"
    topology_tree = node.get("topology_tree")
    template_id = node.get("template_id") or ""
    header = _file_header(node)
    if template_id:
        header = header.replace(
            f"# topology: {topology}\n",
            f"# topology: {topology}\n# template_id: {template_id}\n",
        )
    pkg = node.get("function_name") or "package"
    if not children:
        return header + f"def {pkg}(ctx):\n    return ctx\n"
    lines = [header]
    for child in children:
        lines.append(f"{_import_child(child['function_name'])}\n")
    lines.append(f"\ndef {pkg}(ctx):\n")
    lines.extend((f"{line}\n" for line in emit_flow(children, topology, topology_tree)))
    return "".join(lines)
