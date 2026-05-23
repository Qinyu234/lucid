from pathlib import Path

from src.config.load_app_config import OUTPUT_DIR, _DEFAULT_APP, load_app_config


def get_output_dir() -> Path:
    return Path(load_app_config().get("output_dir", _DEFAULT_APP["output_dir"]))
