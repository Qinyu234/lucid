from src.schema.io.format_io_side import format_io_side
from src.schema.io.normalize_io import normalize_io


def format_io_comment(io: dict) -> tuple:
    io = normalize_io(io)
    return format_io_side(io, "in"), format_io_side(io, "out")
