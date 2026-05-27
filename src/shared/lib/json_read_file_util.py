def json_read_file_util(path: str, default):
    import json
    from pathlib import Path

    p = Path(path)
    if not p.exists():
        return default
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

