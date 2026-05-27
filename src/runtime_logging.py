def runtime_logging(ctx):
    from src.shared.logging.get_logger_util import get_logger_util
    from src.shared.logging.event_util import event_util
    from src.shared.logging.setup_util import setup_util

    setup_util()
    meta = ctx.setdefault("meta", {})
    meta["logger"] = get_logger_util()
    meta["event_util"] = event_util
    return ctx
