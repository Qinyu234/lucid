import json
from datetime import datetime, timezone
from pathlib import Path

from src.config import load_app_config


def memory_path() -> Path:
    cfg = load_app_config()
    path = Path(cfg.get("memory_file", "io/output/memory/leaves.json"))
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def shared_dir() -> Path:
    cfg = load_app_config()
    path = Path(cfg.get("shared_dir", "io/output/shared"))
    path.mkdir(parents=True, exist_ok=True)
    init_py = path / "__init__.py"
    if not init_py.exists():
        init_py.write_text("", encoding="utf-8")
    return path


def load_entries() -> list:
    path = memory_path()
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def save_entries(entries: list):
    with memory_path().open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
