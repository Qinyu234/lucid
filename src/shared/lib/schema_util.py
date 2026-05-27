def schema_util(name: str) -> dict:
    import json
    from pathlib import Path
    from src.shared.lib.app_config_util import app_config_util
    if not hasattr(schema_util, "_cache"):
        schema_util._cache = {}
    cache = schema_util._cache

    def schema_dir():
        cfg = app_config_util()
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
