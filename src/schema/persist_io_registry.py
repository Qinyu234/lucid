import json
from datetime import datetime, timezone
from pathlib import Path

from src.config.load_app_config import load_app_config
from src.schema.register_tree_io import register_tree_io


def persist_io_registry(root: dict, job: dict):

    def _registry_paths(job: dict | None = None) -> tuple:
        cfg = load_app_config()
        global_path = Path(cfg.get("schema_dir", "io/schema")) / "type_registry.json"

        job_path = None
        if job and job.get("root_path"):
            job_path = Path(job["root_path"]) / "tree" / "io_registry.json"

        return global_path, job_path

    def _load_registry(path: Path) -> dict:
        if not path.exists():
            return {"fields": {}, "modules": {}}
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("fields", {})
        data.setdefault("modules", {})
        return data

    def _save_registry(path: Path, data: dict):
        path.parent.mkdir(parents=True, exist_ok=True)
        data["updated"] = datetime.now(timezone.utc).isoformat()
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    registry = register_tree_io(root, job)

    global_path, job_path = _registry_paths(job)

    global_reg = _load_registry(global_path)
    for name, meta in registry["fields"].items():
        g = global_reg["fields"].setdefault(name, {"type": meta.get("type", "any")})
        if meta.get("type") and meta["type"] != "any":
            g["type"] = meta["type"]
        g["produced_by"] = meta.get("produced_by", [])
        g["consumed_by"] = meta.get("consumed_by", [])
        g["used_by"] = meta.get("used_by", [])

    global_reg["modules"].update(registry["modules"])
    _save_registry(global_path, global_reg)

    if job_path:
        _save_registry(job_path, registry)

    return registry
