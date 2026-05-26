def save_entries(entries: list):
    import json
    from src.pipeline.memory.memory_path import memory_path
    with memory_path().open('w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
