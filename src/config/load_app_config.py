from pathlib import Path

from src.config.load_json import load_json

CONFIG_DIR = Path("config")
_APP_PATH = CONFIG_DIR / "app_config.json"
OUTPUT_DIR = Path("io/output")

_DEFAULT_APP = {
    "output_dir": str(OUTPUT_DIR),
    "shared_dir": str(OUTPUT_DIR / "shared"),
    "memory_file": str(OUTPUT_DIR / "memory" / "leaves.json"),
    "logs_dir": str(OUTPUT_DIR / "logs"),
    "schema_dir": "io/schema",
    "growth": {
        "max_depth": 4,
        "max_loop_iters": 20,
        "max_expand_fail": 3,
        "max_frontier_per_iter": 8,
        "naming_use_llm": False,
        "similarity_threshold": 0.85,
    },
    "tree_store": {
        "enabled": True,
        "subdir": "tree",
        "keep_history": True,
        "max_history": 100,
    },
    "memory": {
        "retrieve_top_k": 10,
        "rerank_top_k": 5,
        "keyword_weight": 0.35,
        "embedding_weight": 0.65,
        "embedding_min_score": 0.4,
        "rerank_min_score": -2.0,
        "io_require_out_subset": True,
        "io_require_in_overlap": True,
    },
    "memory_reranker_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
    "tests": {
        "enabled": True,
        "write_conftest": True,
    },
}


def load_app_config() -> dict:
    return load_json(_APP_PATH, _DEFAULT_APP)
