from src.schema.io.normalize_io import normalize_io


def io_in_names(io: dict) -> list:
    return [f["name"] for f in normalize_io(io).get("in", [])]
