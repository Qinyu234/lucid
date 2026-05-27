def tree_dir_util(job: dict) -> str:
    from pathlib import Path

    from src.shared.lib.app_config_util import app_config_util

    cfg = app_config_util().get("tree_store", {})
    subdir = cfg.get("subdir", "tree")
    root = Path(job.get("root_path", "io/output/workplace/unknown"))
    path = root / subdir
    path.mkdir(parents=True, exist_ok=True)
    return str(path).replace("\\", "/")
