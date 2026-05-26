def format_io_side(io: dict, side: str) -> str:
    from src.shared.normalize_io import normalize_io
    io = normalize_io(io)
    parts = [f"{f['name']}:{f['type']}" for f in io.get(side, [])]
    return ', '.join(parts) if parts else '(none)'
