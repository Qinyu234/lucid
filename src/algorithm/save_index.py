import json
from datetime import datetime, timezone

from src.algorithm.algorithm_dir import algorithm_dir


def save_index(data: dict):
    path = algorithm_dir() / "index.json"
    data.setdefault("algorithms", {})
    data.setdefault("categories", {})
    data["updated"] = datetime.now(timezone.utc).isoformat()
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
