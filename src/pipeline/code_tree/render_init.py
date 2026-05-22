from typing import Any


def _io_comment(node: dict) -> str:
    io = node.get("io") or {}
    return (
        f"# io.in: {io.get('in', [])}\n"
        f"# io.out: {io.get('out', [])}\n"
    )


def _import_run(module_name: str) -> str:
    return f"from .{module_name} import run as _run_{module_name}"


def _render_seq(children: list, header: str) -> str:
    lines = [header, "from typing import Any\n\n", "def run(ctx: dict[str, Any]) -> dict[str, Any]:\n"]

    for child in children:
        fn = child["function_name"]
        alias = f"_run_{fn}"
        lines.append(f"    {_import_run(fn)}\n")
        lines.append(f"    ctx = {alias}(ctx)\n")

    lines.append("    return ctx\n")
    return "".join(lines)


def _render_router(children: list, header: str) -> str:
    lines = [
        header,
        "from typing import Any\n\n",
        "def run(ctx: dict[str, Any]) -> dict[str, Any]:\n",
        '    meta = ctx.setdefault("meta", {})\n',
        '    case = meta.get("case")\n',
        "    if case is None:\n",
    ]

    default = children[0]
    default_fn = default["function_name"]
    lines.append(f"        {_import_run(default_fn)}\n")
    lines.append(f"        return _run_{default_fn}(ctx)\n")

    for child in children:
        fn = child["function_name"]
        case_id = child.get("case") or "CASE_0"
        lines.append(f'    if case == "{case_id}":\n')
        lines.append(f"        {_import_run(fn)}\n")
        lines.append(f"        return _run_{fn}(ctx)\n")

    lines.append("    return ctx\n")
    return "".join(lines)


def render_init(node: dict) -> str:

    children = node.get("children", [])
    topology = node.get("topology") or "SEQ"
    header = _io_comment(node)

    if not children:
        return (
            header
            + "from typing import Any\n\n"
            + "def run(ctx: dict[str, Any]) -> dict[str, Any]:\n"
            + "    return ctx\n"
        )

    if topology == "ROUTER":
        return _render_router(children, header)

    return _render_seq(children, header)
