def load_jobs_util(path: str = "io/input/idea_list.json") -> dict:
    from src.shared.lib.json_read_file_util import json_read_file_util
    from src.shared.lib.path_exists_util import path_exists_util
    from src.shared.logging.get_logger_util import get_logger_util

    logger = get_logger_util()
    if not path_exists_util(path):
        logger.error("input file not found: %s", path)
        raise SystemExit(f"file not found: {path}")
    data = json_read_file_util(path, default={})
    if not isinstance(data, dict):
        logger.error("invalid JSON root: %s", path)
        raise SystemExit(f"invalid JSON format: {path}")
    logger.info("loaded input %s jobs=%s", path, len(data.get("jobs", []) if isinstance(data.get("jobs"), list) else []))
    return data

