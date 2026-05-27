def io_format_side_util(io: dict, side: str) -> str:
    from src.shared.validate.io_normalize_util import io_normalize_util
    io = io_normalize_util(io)
    parts = [f"{f['name']}:{f['type']}" for f in io.get(side, [])]
    return ', '.join(parts) if parts else '(none)'
