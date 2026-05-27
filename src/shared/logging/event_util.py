def event_util(logger, event, level=None, **fields):
    import json
    import logging
    from datetime import datetime, timezone

    if level is None:
        level = logging.INFO

    def json_safe(value):
        if isinstance(value, dict):
            return {k: json_safe(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [json_safe(v) for v in value]
        if hasattr(value, "item") and callable(value.item):
            return value.item()
        return value

    payload = {
        "event": event,
        "ts": datetime.now(timezone.utc).isoformat(),
        **{k: json_safe(v) for k, v in fields.items()},
    }
    logger.log(level, json.dumps(payload, ensure_ascii=False))
