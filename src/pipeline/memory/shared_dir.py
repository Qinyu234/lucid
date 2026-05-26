def shared_dir():
    from pathlib import Path

    from src.shared.load_app_config import load_app_config

    cfg = load_app_config()
    path = Path(cfg.get('shared_dir', 'io/output/shared'))
    path.mkdir(parents=True, exist_ok=True)
    init_py = path / '__init__.py'
    if not init_py.exists():
        init_py.write_text('', encoding='utf-8')
    return path
