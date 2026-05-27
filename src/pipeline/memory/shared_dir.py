def shared_dir():
    from src.shared.lib.app_config_util import app_config_util
    from src.shared.lib.path_write_text_util import path_write_text_util

    cfg = app_config_util()
    path = str(cfg.get("shared_dir", "io/output/shared"))
    init_py = path.rstrip("/").rstrip("\\") + "/__init__.py"
    path_write_text_util(init_py, "")
    return path
