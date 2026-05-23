from src.schema.io.normalize_io import normalize_io


def format_io_side(io: dict, side: str) -> str:
    io = normalize_io(io)
    parts = [f"{f['name']}:{f['type']}" for f in io.get(side, [])]
    return ", ".join(parts) if parts else "(none)"
