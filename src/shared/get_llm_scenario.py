def get_llm_scenario(name):
    from src.shared.load_llm_config import load_llm_config

    cfg = load_llm_config()
    scenarios = cfg.get("scenarios") or {}
    base = {
        "api_url": cfg.get("default_api_url"),
        "model": cfg.get("default_model"),
        "timeout_sec": 900,
    }
    if name in scenarios:
        merged = dict(base)
        merged.update(scenarios[name] or {})
        if "api_url" not in merged and cfg.get("default_api_url"):
            merged["api_url"] = cfg.get("default_api_url")
        if "model" not in merged and cfg.get("default_model"):
            merged["model"] = cfg.get("default_model")
        return merged
    return base
