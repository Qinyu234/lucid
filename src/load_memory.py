import os
import json

def load_memory(path: str = "output/memory/code_memory.json") -> list:
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 防御：避免文件损坏
    if not isinstance(data, list):
        return []

    return data