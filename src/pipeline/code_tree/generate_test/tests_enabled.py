def tests_enabled() -> bool:
    from src.shared.lib.app_config_util import app_config_util

    cfg = app_config_util().get("tests", {})
    return cfg.get("enabled", True)
