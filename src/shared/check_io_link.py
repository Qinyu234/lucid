def check_io_link(upstream: dict, downstream: dict, label: str='') -> list:
    from src.shared.io_type_map import io_type_map
    '\n    Static check: overlapping keys between upstream.out and downstream.in\n    must have identical types.\n    '
    issues = []
    up_out = io_type_map(upstream, 'out')
    down_in = io_type_map(downstream, 'in')
    prefix = f'{label}: ' if label else ''
    for key in set(up_out) & set(down_in):
        if up_out[key] != down_in[key]:
            issues.append(f"{prefix}type mismatch on '{key}': upstream.out={up_out[key]} vs downstream.in={down_in[key]}")
    for key in down_in:
        if key not in up_out and up_out:
            issues.append(f"{prefix}downstream requires in '{key}:{down_in[key]}' but upstream.out lacks it")
    return issues
