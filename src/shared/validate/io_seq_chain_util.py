def io_seq_chain_util(children: list, strict: bool=False) -> list:
    from src.shared.validate.io_link_util import io_link_util
    from src.shared.validate.io_format_side_util import io_format_side_util
    from src.shared.validate.io_in_names_util import io_in_names_util
    from src.shared.validate.io_out_names_util import io_out_names_util
    issues = []
    for i in range(len(children) - 1):
        left = children[i]
        right = children[i + 1]
        link_issues = io_link_util(left.get('io'), right.get('io'), label=f'step[{i}]->step[{i + 1}]')
        issues.extend(link_issues)
        if not link_issues:
            out_names = set(io_out_names_util(left.get('io')))
            in_names = set(io_in_names_util(right.get('io')))
            if out_names and in_names and (not out_names & in_names):
                issues.append(f"step[{i}]->step[{i + 1}]: no shared keys between out({io_format_side_util(left.get('io'), 'out')}) and in({io_format_side_util(right.get('io'), 'in')})")
    return issues
