def tree_dir(job: dict):
    from pathlib import Path

    from src.shared.load_app_config import load_app_config

    cfg = load_app_config().get('tree_store', {})
    subdir = cfg.get('subdir', 'tree')
    root = Path(job.get('root_path', 'io/output/workplace/unknown'))
    path = root / subdir
    path.mkdir(parents=True, exist_ok=True)
    return path
