def io_type_map_util(io: dict, side: str) -> dict:
    from src.shared.validate.io_normalize_util import io_normalize_util
    io = io_normalize_util(io)
    fields = io.get(side, [])
    return {f['name']: f['type'] for f in fields}
