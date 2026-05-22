import json
from pathlib import Path

CONFIG_DIR = Path("config")
_LLM_PATH = CONFIG_DIR / "llm_config.json"
_APP_PATH = CONFIG_DIR / "app_config.json"

OUTPUT_DIR = Path("io/output")

_DEFAULT_LLM = {
    "default_api_url": "http://localhost:11434/api/generate",
    "default_model": "qwen2.5-coder",
    "scenarios": {},
}

_DEFAULT_APP = {
    "output_dir": str(OUTPUT_DIR),
    "shared_dir": str(OUTPUT_DIR / "shared"),
    "memory_file": str(OUTPUT_DIR / "memory" / "leaves.json"),
    "logs_dir": str(OUTPUT_DIR / "logs"),
    "memory_similarity": 0.88,
    "schema_dir": "io/schema",
}


def _load_json(path: Path, default: dict) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", encoding="utf-8") as f:
            json.dump(default, f, indent=2, ensure_ascii=False)
        return dict(default)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_llm_config() -> dict:
    return _load_json(_LLM_PATH, _DEFAULT_LLM)


def load_app_config() -> dict:
    return _load_json(_APP_PATH, _DEFAULT_APP)


def get_output_dir() -> Path:
    return Path(load_app_config().get("output_dir", _DEFAULT_APP["output_dir"]))


def get_logs_dir() -> Path:
    cfg = load_app_config()
    return Path(cfg.get("logs_dir", _DEFAULT_APP["logs_dir"]))


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
