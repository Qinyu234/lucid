import json
from datetime import datetime, timezone
from pathlib import Path

from src.config.load_app_config import load_app_config


def memory_path() -> Path:
    cfg = load_app_config()
    path = Path(cfg.get("memory_file", "io/output/memory/leaves.json"))
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
