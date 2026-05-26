def load_llm_config():
    from pathlib import Path

    from src.shared.load_json import load_json

    llm_path = Path("io/input") / "llm_config.json"
    default_llm = {
        "default_api_url": "http://localhost:11434/api/generate",
        "default_model": "qwen2.5-coder",
        "scenarios": {},
    }
    return load_json(llm_path, default_llm)
