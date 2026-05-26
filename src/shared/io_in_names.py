def io_in_names(io: dict) -> list:
    from src.shared.normalize_io import normalize_io
    return [f['name'] for f in normalize_io(io).get('in', [])]
