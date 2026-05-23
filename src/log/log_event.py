import json
import logging
from datetime import datetime, timezone


def log_event(logger: logging.Logger, event: str, level: int = logging.INFO, **fields):
    payload = {
        "event": event,
        "ts": datetime.now(timezone.utc).isoformat(),
        **fields,
    }
    logger.log(level, json.dumps(payload, ensure_ascii=False))
