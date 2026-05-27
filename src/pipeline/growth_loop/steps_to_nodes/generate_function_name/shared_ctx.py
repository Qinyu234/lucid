def shared_ctx(ctx):
    from src.shared.lib.app_config_util import app_config_util

    meta = ctx.setdefault("meta", {})
    meta["app_config_util"] = app_config_util
    return ctx
