def algorithm_dir():
    from pathlib import Path

    from src.shared.load_app_config import load_app_config

    cfg = load_app_config()
    path = Path(cfg.get('algorithm_dir', 'io/output/algorithm'))
    path.mkdir(parents=True, exist_ok=True)
    init_py = path / '__init__.py'
    if not init_py.exists():
        init_py.write_text('"""Optimized algorithm library (info-theory aware)."""\n', encoding='utf-8')
    return path
