def load_entries() -> list:
    from src.shared.lib.app_config_util import app_config_util
    from src.shared.lib.json_read_file_util import json_read_file_util
    from src.shared.lib.path_exists_util import path_exists_util

    cfg = app_config_util()
    path = str(cfg.get("memory_file", "io/output/memory/leaves.json"))
    if not path_exists_util(path):
        return []
    data = json_read_file_util(path, default=[])
    return data if isinstance(data, list) else []
