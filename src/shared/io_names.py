def io_names(io: dict) -> list:
    from src.shared.normalize_io import normalize_io
    io = normalize_io(io)
    return [f['name'] for f in io.get('in', []) + io.get('out', [])]
