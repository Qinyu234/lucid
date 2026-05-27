def emit_flow(children: list, topology: str) -> list[str]:
    from src.shared.validate.io_format_side_util import io_format_side_util
    from src.shared.validate.io_in_names_util import io_in_names_util
    from src.shared.validate.io_out_names_util import io_out_names_util
    'Emit __init__ body lines with explicit ctx/data flow.'

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
