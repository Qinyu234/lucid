def shared_ctx(ctx):
    from src.shared.validate.io_empty_util import io_empty_util
    from src.shared.logging.get_logger_util import get_logger_util
    from src.shared.lib.app_config_util import app_config_util
    from src.shared.validate.io_normalize_util import io_normalize_util
    from src.shared.validate.expand_output_util import expand_output_util

    meta = ctx.setdefault("meta", {})
    meta["io_empty_util"] = io_empty_util
    meta["get_logger_util"] = get_logger_util
    meta["app_config_util"] = app_config_util
    meta["io_normalize_util"] = io_normalize_util
    meta["expand_output_util"] = expand_output_util
    return ctx
