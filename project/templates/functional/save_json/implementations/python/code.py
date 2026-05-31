import json
import os

def save_json(inputs: dict, meta: dict) -> dict:
    data = inputs.get("data")
    path = inputs.get("path")

    if data is None:
        raise ValueError("input 'data' is required and cannot be None")
    if path is None:
        raise ValueError("input 'path' is required and cannot be None")
    if not isinstance(path, str):
        raise TypeError(f"input 'path' must be string, got {type(path).__name__}")

    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return { "success": True, "path": path }
