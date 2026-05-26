def format_io_comment(io: dict) -> tuple:
    from src.shared.format_io_side import format_io_side
    from src.shared.normalize_io import normalize_io
    io = normalize_io(io)
    return (format_io_side(io, 'in'), format_io_side(io, 'out'))
