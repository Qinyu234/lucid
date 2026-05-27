def io_context_util(raw_io: dict | None) -> dict:
    """Normalize IO and return display strings for prompts and comments."""

    from src.shared.validate.io_format_comment_util import io_format_comment_util
    from src.shared.validate.io_format_side_util import io_format_side_util
    from src.shared.validate.io_normalize_util import io_normalize_util

    io = io_normalize_util(raw_io)
    in_str, out_str = io_format_comment_util(io)
    return {
        "io": io,
        "io_in": in_str,
        "io_out": out_str,
        "io_in_side": io_format_side_util(io, "in"),
        "io_out_side": io_format_side_util(io, "out"),
    }
