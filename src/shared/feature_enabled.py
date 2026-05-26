def feature_enabled(name):
    from src.shared.load_app_config import load_app_config

    slim_defaults = {
        "memory_recall": False,
        "embedding_split": False,
        "algorithm_catalog": False,
        "algorithm_registry_on_start": False,
        "tree_keep_history": False,
        "ollama_unload_after_request": True,
    }
    feats = load_app_config().get("features", {})
    if name == "embedding_split":
        growth = load_app_config().get("growth", {})
        mode = str(growth.get("split_validation", "") or "").strip().lower()
        if mode:
            return mode == "embedding"
    if name in feats:
        return bool(feats[name])
    if feats.get("slim_mode"):
        return slim_defaults.get(name, True)
    return True
