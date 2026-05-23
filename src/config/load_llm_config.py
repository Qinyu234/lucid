from src.config.load_json import load_json

from .load_app_config import CONFIG_DIR

_LLM_PATH = CONFIG_DIR / "llm_config.json"

_DEFAULT_LLM = {
    "default_api_url": "http://localhost:11434/api/generate",
    "default_model": "qwen2.5-coder",
    "scenarios": {},
}


def load_llm_config() -> dict:
    return load_json(_LLM_PATH, _DEFAULT_LLM)
