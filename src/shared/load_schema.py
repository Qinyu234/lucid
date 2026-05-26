def load_schema(name: str) -> dict:
    import json
    from pathlib import Path
    from src.shared.load_app_config import load_app_config
    if not hasattr(load_schema, "_cache"):
        load_schema._cache = {}
    cache = load_schema._cache

    def schema_dir():
        cfg = load_app_config()
        return Path(cfg.get('schema_dir', 'io/input/schema'))
    if name in cache:
        return cache[name]
    path = schema_dir() / name
    if not path.exists():
        raise FileNotFoundError(f'[SCHEMA] not found: {path}')
    with path.open('r', encoding='utf-8') as f:
        schema = json.load(f)
    cache[name] = schema
    return schema
