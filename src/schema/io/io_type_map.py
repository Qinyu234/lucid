from src.schema.io.normalize_io import normalize_io


def io_type_map(io: dict, side: str) -> dict:
    io = normalize_io(io)
    fields = io.get(side, [])
    return {f["name"]: f["type"] for f in fields}
