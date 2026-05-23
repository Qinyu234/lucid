from pathlib import Path

from src.config.load_app_config import _DEFAULT_APP, load_app_config


def get_logs_dir() -> Path:
    cfg = load_app_config()
    return Path(cfg.get("logs_dir", _DEFAULT_APP["logs_dir"]))
