def shared_ctx(ctx):
    from src.shared.lib.feature_util import feature_util
    from src.shared.logging.get_logger_util import get_logger_util
    from src.shared.logging.event_util import event_util
    from src.shared.io_tree.persist_registry_util import persist_registry_util
    from src.shared.validate.node_schema_util import node_schema_util

    meta = ctx.setdefault("meta", {})
    meta["feature_util"] = feature_util
    meta["get_logger_util"] = get_logger_util
    meta["event_util"] = event_util
    meta["persist_registry_util"] = persist_registry_util
    meta["node_schema_util"] = node_schema_util
    return ctx
