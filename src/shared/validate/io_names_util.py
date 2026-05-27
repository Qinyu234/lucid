def io_names_util(io: dict) -> list:
    from src.shared.validate.io_normalize_util import io_normalize_util
    io = io_normalize_util(io)
    return [f['name'] for f in io.get('in', []) + io.get('out', [])]
