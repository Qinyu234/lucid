def save_entries(entries: list):
    from src.shared.lib.app_config_util import app_config_util
    from src.shared.lib.json_write_file_util import json_write_file_util

    cfg = app_config_util()
    path = str(cfg.get("memory_file", "io/output/memory/leaves.json"))
    json_write_file_util(path, entries)
