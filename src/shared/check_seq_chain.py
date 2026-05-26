def check_seq_chain(children: list, strict: bool=False) -> list:
    from src.shared.check_io_link import check_io_link
    from src.shared.format_io_side import format_io_side
    from src.shared.io_in_names import io_in_names
    from src.shared.io_out_names import io_out_names
    issues = []
    for i in range(len(children) - 1):
        left = children[i]
        right = children[i + 1]
        link_issues = check_io_link(left.get('io'), right.get('io'), label=f'step[{i}]->step[{i + 1}]')
        issues.extend(link_issues)
        if not link_issues:
            out_names = set(io_out_names(left.get('io')))
            in_names = set(io_in_names(right.get('io')))
            if out_names and in_names and (not out_names & in_names):
                issues.append(f"step[{i}]->step[{i + 1}]: no shared keys between out({format_io_side(left.get('io'), 'out')}) and in({format_io_side(right.get('io'), 'in')})")
    return issues
