def feature_util(name):
    from src.shared.lib.app_config_util import app_config_util

    slim_defaults = {
        "memory_recall": False,
        "embedding_split": False,
        "tree_keep_history": False,
        "ollama_unload_after_request": True,
    }
    feats = app_config_util().get("features", {})
    if name == "embedding_split":
        growth = app_config_util().get("growth", {})
        mode = str(growth.get("split_validation", "") or "").strip().lower()
        if mode:
            return mode == "embedding"
    if name in feats:
        return bool(feats[name])
    if feats.get("slim_mode"):
        return slim_defaults.get(name, True)
    return True
