def llm_config_util():
    from pathlib import Path

    from src.shared.lib.json_util import json_util

    llm_path = Path("io/input") / "llm_config.json"
    default_llm = {
        "default_api_url": "http://localhost:11434/api/generate",
        "default_model": "qwen2.5-coder",
        "scenarios": {},
    }
    return json_util(llm_path, default_llm)
