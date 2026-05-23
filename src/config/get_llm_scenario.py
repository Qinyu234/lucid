from src.config.load_llm_config import load_llm_config


def get_llm_scenario(name: str) -> dict:
    cfg = load_llm_config()
    base = {
        "api_url": cfg.get("default_api_url"),
        "model": cfg.get("default_model"),
        "timeout_sec": 120,
        "format": None,
    }
    scenario = cfg.get("scenarios", {}).get(name, {})
    return {**base, **scenario}
