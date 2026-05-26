def load_entries() -> list:
    import json
    from src.pipeline.memory.memory_path import memory_path
    path = memory_path()
    if not path.exists():
        return []
    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return data if isinstance(data, list) else []
