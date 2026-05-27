def io_merge_seq_util(children: list) -> dict:
    from src.shared.validate.io_empty_util import io_empty_util
    from src.shared.validate.io_normalize_util import io_normalize_util
    if not children:
        return io_empty_util()
    first = io_normalize_util(children[0].get('io'))
    last = io_normalize_util(children[-1].get('io'))
    return {'in': first['in'], 'out': last['out']}
