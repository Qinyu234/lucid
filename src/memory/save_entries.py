import json

from src.memory.memory_path import memory_path


def save_entries(entries: list):
    with memory_path().open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
