def get_output_dir():
    from pathlib import Path

    from src.shared.load_app_config import load_app_config

    cfg = load_app_config()
    return Path(cfg.get("output_dir", "io/output"))
