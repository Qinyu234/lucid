import json

from src.memory.memory_path import memory_path


def load_entries() -> list:
    path = memory_path()
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []
