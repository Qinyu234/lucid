def io_format_comment_util(io: dict) -> tuple:
    from src.shared.validate.io_format_side_util import io_format_side_util
    from src.shared.validate.io_normalize_util import io_normalize_util
    io = io_normalize_util(io)
    return (io_format_side_util(io, 'in'), io_format_side_util(io, 'out'))
