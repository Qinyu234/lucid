def setup_util(job_id=None):
    import logging
    import sys
    from datetime import datetime, timezone

    from src.shared.lib.logs_dir_util import logs_dir_util

    if not hasattr(setup_util, "_initialized"):
        setup_util._initialized = False

    log_dir = logs_dir_util()
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

    if not setup_util._initialized:
        logger.info("logging initialized file=%s", log_file)
        setup_util._initialized = True

    return logger
