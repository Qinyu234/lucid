from src.schema.io.format_io_comment import format_io_comment


def render_init(node: dict) -> str:

    def _import_child(fn: str) -> str:
        return f"from .{fn} import {fn}"

    def _file_header(node: dict) -> str:
        io_in, io_out = format_io_comment(node.get("io"))
        return (
            f"# semantic: {node.get('semantic', '')}\n"
            f"# io.in: {io_in}\n"
            f"# io.out: {io_out}\n"
            f"# topology: {node.get('topology') or 'SEQ'}\n\n"
        )

    def _render_seq(node: dict, children: list, header: str) -> str:
        pkg = node["function_name"]
        lines = [header]

        for child in children:
            lines.append(f"{_import_child(child['function_name'])}\n")

        lines.append(f"\ndef {pkg}(ctx):\n")
        for child in children:
            fn = child["function_name"]
            lines.append(f"    ctx = {fn}(ctx)\n")
        lines.append("    return ctx\n")
        return "".join(lines)

    def _render_router(node: dict, children: list, header: str) -> str:
        pkg = node["function_name"]
        lines = [header]

        for child in children:
            lines.append(f"{_import_child(child['function_name'])}\n")

        default = children[0]["function_name"]
        lines.append(f"\ndef {pkg}(ctx):\n")
        lines.append('    meta = ctx.setdefault("meta", {})\n')
        lines.append('    case = meta.get("case")\n')
        lines.append("    if case is None:\n")
        lines.append(f"        return {default}(ctx)\n")

        for child in children:
            fn = child["function_name"]
            case_id = child.get("case") or "CASE_0"
            lines.append(f'    if case == "{case_id}":\n')
            lines.append(f"        return {fn}(ctx)\n")

        lines.append(f"    return {default}(ctx)\n")
        return "".join(lines)

    def _render_par(node: dict, children: list, header: str) -> str:
        """PAR stub: invoke all branches on same ctx (sequential, no thread)."""
        pkg = node["function_name"]
        lines = [header]

        for child in children:
            lines.append(f"from .{child['function_name']} import {child['function_name']}\n")

        lines.append(f"\ndef {pkg}(ctx):\n")
        for child in children:
            fn = child["function_name"]
            lines.append(f"    ctx = {fn}(ctx)\n")
        lines.append("    return ctx\n")
        return "".join(lines)

    children = node.get("children", [])
    topology = node.get("topology") or "SEQ"
    header = _file_header(node)
    pkg = node.get("function_name") or "package"

    if not children:
        return header + f"def {pkg}(ctx):\n    return ctx\n"

    if topology == "ROUTER":
        return _render_router(node, children, header)

    if topology == "PAR":
        return _render_par(node, children, header)

    return _render_seq(node, children, header)
