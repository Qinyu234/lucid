import logging
import sys
from datetime import datetime, timezone

from src.config.get_logs_dir import get_logs_dir

_INITIALIZED = False


def setup_logging(job_id: str | None = None) -> logging.Logger:
    global _INITIALIZED

    log_dir = get_logs_dir()
    log_dir.mkdir(parents=True, exist_ok=True)

    name = "code_generator" if not job_id else f"code_generator.{job_id}"
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)
    logger.addHandler(console)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = job_id or "main"
    log_file = log_dir / f"run_{suffix}_{stamp}.log"

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    if not _INITIALIZED:
        logger.info("logging initialized file=%s", log_file)
        _INITIALIZED = True

    return logger
