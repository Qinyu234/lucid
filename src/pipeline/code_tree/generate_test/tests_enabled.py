from src.shared.load_app_config import load_app_config


def tests_enabled() -> bool:
    cfg = load_app_config().get("tests", {})
    return cfg.get("enabled", True)
