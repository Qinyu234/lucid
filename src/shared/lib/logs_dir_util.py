def logs_dir_util():
    from pathlib import Path

    from src.shared.lib.app_config_util import app_config_util

    cfg = app_config_util()
    return Path(cfg.get("logs_dir", "io/output/logs"))
