def get_logs_dir():
    from pathlib import Path

    from src.shared.load_app_config import load_app_config

    cfg = load_app_config()
    return Path(cfg.get("logs_dir", "io/output/logs"))
