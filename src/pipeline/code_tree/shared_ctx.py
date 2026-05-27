def shared_ctx(ctx):
    from src.shared.logging.get_logger_util import get_logger_util
    from src.shared.lib.app_config_util import app_config_util
    from src.shared.logging.event_util import event_util

    meta = ctx.setdefault("meta", {})
    meta["get_logger_util"] = get_logger_util
    meta["app_config_util"] = app_config_util
    meta["event_util"] = event_util
    return ctx
