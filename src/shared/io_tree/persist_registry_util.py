def persist_registry_util(root: dict, job: dict):
    import json
    from datetime import datetime, timezone
    from pathlib import Path

    from src.shared.lib.app_config_util import app_config_util
    from src.shared.io_tree.register_util import register_util

    cfg = app_config_util()
    global_path = Path(cfg.get("schema_dir", "io/input/schema")) / "type_registry.json"
    job_path = None
    if job and job.get("root_path"):
        job_path = Path(job["root_path"]) / "tree" / "io_registry.json"

    def _load(path: Path) -> dict:
        if not path.exists():
            return {"fields": {}, "modules": {}}
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("fields", {})
        data.setdefault("modules", {})
        return data

    def _save(path: Path, data: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data["updated"] = datetime.now(timezone.utc).isoformat()
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    registry = register_util(root, job)
    global_reg = _load(global_path)
    for name, meta in registry.get("fields", {}).items():
        g = global_reg["fields"].setdefault(name, {"type": meta.get("type", "any")})
        if meta.get("type") and meta["type"] != "any":
            g["type"] = meta["type"]
        g["produced_by"] = meta.get("produced_by", [])
        g["consumed_by"] = meta.get("consumed_by", [])
        g["used_by"] = meta.get("used_by", [])
    global_reg["modules"].update(registry.get("modules", {}))
    _save(global_path, global_reg)
    if job_path:
        _save(job_path, registry)
    return registry

