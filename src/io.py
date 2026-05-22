import json
from pathlib import Path

from .errors import IOError, error_packet
from .log import get_logger


def io(path: str = "io/input/idea_list.json") -> dict:

    logger = get_logger()
    file_path = Path(path)

    if not file_path.exists():
        logger.error("input file not found: %s", file_path)
        raise IOError(f"file not found: {file_path}")

    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

    except json.JSONDecodeError as e:
        logger.error("invalid JSON: %s", e)
        raise IOError(f"invalid JSON format: {e}") from e

    except Exception as e:
        logger.exception("unexpected read error")
        raise IOError(f"unexpected error: {e}") from e

    logger.info("loaded input %s jobs=%s", file_path, len(data.get("jobs", [])))
    return data
