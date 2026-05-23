from src.schema.io.normalize_io import normalize_io


def io_names(io: dict) -> list:
    io = normalize_io(io)
    return [f["name"] for f in io.get("in", []) + io.get("out", [])]
