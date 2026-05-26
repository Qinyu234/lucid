def io_type_map(io: dict, side: str) -> dict:
    from src.shared.normalize_io import normalize_io
    io = normalize_io(io)
    fields = io.get(side, [])
    return {f['name']: f['type'] for f in fields}
