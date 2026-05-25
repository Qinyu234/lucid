import json
from pathlib import Path

from src.algorithm.algorithm_dir import algorithm_dir


def load_index() -> dict:
    path = algorithm_dir() / "index.json"
    if not path.exists():
        return {"algorithms": {}, "categories": {}}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("algorithms", {})
    data.setdefault("categories", {})
    return data
