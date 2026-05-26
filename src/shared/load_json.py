def load_json(path, default):
    import json
    from pathlib import Path

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        with p.open("w", encoding="utf-8") as f:
            json.dump(default, f, indent=2, ensure_ascii=False)
        return dict(default)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)
