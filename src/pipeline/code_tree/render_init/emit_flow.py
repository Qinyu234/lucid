def emit_flow(children: list, topology: str, topology_tree: dict | None = None) -> list[str]:
    from src.shared.validate.io_format_side_util import io_format_side_util
    from src.shared.validate.io_in_names_util import io_in_names_util
    from src.shared.validate.io_out_names_util import io_out_names_util
    'Emit __init__ body lines: flat topology or unit-composed topology_tree.'

    def emit_from_tree(tree: dict) -> list[str]:
        out_lines: list[str] = []

        def child_at(i: int) -> dict:
            return children[int(i)]

        def emit_leaf(i: int, prev_out: set[str], chain: bool) -> set[str]:
            child = child_at(i)
            fn = child['function_name']
            io = child.get('io') or {}
            in_s = io_format_side_util(io, 'in')
            out_s = io_format_side_util(io, 'out')
            in_keys = io_in_names_util(io)
            tag = 'flow' if chain else 'par'
            out_lines.append(f'    # {tag}[{i}] {fn}: in({in_s}) -> out({out_s})')
            if chain and in_keys:
                for key in in_keys:
                    if key in prev_out:
                        out_lines.append(f'    assert "{key}" in data, "missing data[{key!r}] before {fn}"')
            out_lines.append(f'    ctx = {fn}(ctx)')
            out_lines.append('    data = ctx["data"]')
            out_lines.append('')
            return set(io_out_names_util(io))

        def flatten_leaves(node) -> list:
            if isinstance(node, int):
                return [child_at(node)]
            leaves = []
            for arg in node.get('args') or []:
                leaves.extend(flatten_leaves(arg))
            return leaves

        def emit_router_args(args: list) -> None:
            branch_children = []
            for arg in args:
                branch_children.extend(flatten_leaves(arg) if isinstance(arg, dict) else [child_at(arg)])
            default = branch_children[0]['function_name']
            out_lines.extend(['    case = meta.get("case")', '', '    if case is None:', f'        return {default}(ctx)', ''])
            for i, child in enumerate(branch_children):
                fn = child['function_name']
                case_id = child.get('case') or f'CASE_{i}'
                io = child.get('io') or {}
                in_s = io_format_side_util(io, 'in')
                out_s = io_format_side_util(io, 'out')
                out_lines.append(f'    if case == "{case_id}":')
                out_lines.append(f'        # branch {fn}: in({in_s}) -> out({out_s})')
                out_lines.append(f'        return {fn}(ctx)')
            out_lines.append(f'    return {default}(ctx)')
            out_lines.append('')

        def emit_arg(arg, prev_out: set[str], chain: bool) -> set[str]:
            if isinstance(arg, int):
                return emit_leaf(arg, prev_out, chain)
            op = str(arg.get('op', 'SEQ')).upper()
            sub = arg.get('args') or []
            if op == 'SEQ':
                for item in sub:
                    prev_out = emit_arg(item, prev_out, chain=True)
                return prev_out
            if op == 'PAR':
                for item in sub:
                    emit_arg(item, set(), chain=False)
                return prev_out
            emit_router_args(sub)
            return prev_out

        root_op = str(tree.get('op', 'SEQ')).upper()
        root_args = tree.get('args') or list(range(len(children)))
        out_lines.extend(
            [
                '    data = ctx.setdefault("data", {})',
                '    meta = ctx.setdefault("meta", {})',
                '    state = ctx.setdefault("state", {})',
                '    ctx.setdefault("error", None)',
                f'    # template units composed (root {root_op})',
                '',
            ]
        )
        if root_op == 'ROUTER':
            emit_router_args(root_args)
        elif root_op == 'PAR':
            for item in root_args:
                emit_arg(item, set(), chain=False)
        else:
            for item in root_args:
                emit_arg(item, set(), chain=True)
        out_lines.append('    return ctx')
        return out_lines

    if isinstance(topology_tree, dict) and topology_tree.get('args') is not None:
        return emit_from_tree(topology_tree)

    def emit_seq(child_list: list) -> list[str]:
        out_lines = []
        prev_out: set[str] = set()
        for i, child in enumerate(child_list):
            fn = child['function_name']
            io = child.get('io') or {}
            in_s = io_format_side_util(io, 'in')
            out_s = io_format_side_util(io, 'out')
            in_keys = io_in_names_util(io)
            out_lines.append(f'    # flow[{i}] {fn}: in({in_s}) -> out({out_s})')
            if i > 0 and in_keys:
                for key in in_keys:
                    if key in prev_out:
                        out_lines.append(f'    assert "{key}" in data, "missing data[{key!r}] before {fn}"')
            for key in in_keys:
                out_lines.append(f'    #   read  ctx["data"]["{key}"]')
            out_lines.append(f'    ctx = {fn}(ctx)')
            out_lines.append('    data = ctx["data"]')
            for key in io_out_names_util(io):
                out_lines.append(f'    #   write ctx["data"]["{key}"]')
            if i < len(child_list) - 1:
                next_in = io_in_names_util(child_list[i + 1].get('io') or {})
                shared = set(io_out_names_util(io)) & set(next_in)
                if shared:
                    flow = ', '.join((f'"{k}"' for k in sorted(shared)))
                    out_lines.append(f'    #   link -> next: {flow}')
            prev_out = set(io_out_names_util(io))
            out_lines.append('')
        return out_lines

    def emit_par(child_list: list) -> list[str]:
        out_lines = []
        for i, child in enumerate(child_list):
            fn = child['function_name']
            io = child.get('io') or {}
            in_s = io_format_side_util(io, 'in')
            out_s = io_format_side_util(io, 'out')
            out_lines.append(f'    # par[{i}] {fn}: in({in_s}) -> out({out_s})')
            out_lines.append(f'    ctx = {fn}(ctx)')
            out_lines.append('    data = ctx["data"]')
            out_lines.append('')
        return out_lines

    def emit_router(child_list: list) -> list[str]:
        default = child_list[0]['function_name']
        out_lines = ['    case = meta.get("case")', '', '    if case is None:', f'        return {default}(ctx)', '']
        for i, child in enumerate(child_list):
            fn = child['function_name']
            case_id = child.get('case') or f'CASE_{i}'
            io = child.get('io') or {}
            in_s = io_format_side_util(io, 'in')
            out_s = io_format_side_util(io, 'out')
            out_lines.append(f'    if case == "{case_id}":')
            out_lines.append(f'        # branch {fn}: in({in_s}) -> out({out_s})')
            out_lines.append(f'        return {fn}(ctx)')
        out_lines.append(f'    return {default}(ctx)')
        out_lines.append('')
        return out_lines
    lines = ['    data = ctx.setdefault("data", {})', '    meta = ctx.setdefault("meta", {})', '    state = ctx.setdefault("state", {})', '    ctx.setdefault("error", None)', '']
    if topology == 'SEQ':
        lines.extend(emit_seq(children))
    elif topology == 'PAR':
        lines.extend(emit_par(children))
    elif topology == 'ROUTER':
        lines.extend(emit_router(children))
    else:
        lines.extend(emit_seq(children))
    lines.append('    return ctx')
    return lines
