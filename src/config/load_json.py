import json
from pathlib import Path


def load_json(path: Path, default: dict) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", encoding="utf-8") as f:
            json.dump(default, f, indent=2, ensure_ascii=False)
        return dict(default)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
