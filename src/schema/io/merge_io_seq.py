from src.schema.io.empty_io import empty_io
from src.schema.io.normalize_io import normalize_io


def merge_io_seq(children: list) -> dict:
    if not children:
        return empty_io()
    first = normalize_io(children[0].get("io"))
    last = normalize_io(children[-1].get("io"))
    return {"in": first["in"], "out": last["out"]}
