def load_app_config():
    from pathlib import Path

    from src.shared.load_json import load_json

    config_dir = Path("io/input")
    app_path = config_dir / "app_config.json"
    output_dir = Path("io/output")
    default_app = {
        "output_dir": str(output_dir),
        "shared_dir": str(output_dir / "shared"),
        "algorithm_dir": str(output_dir / "algorithm"),
        "algorithm_index": str(output_dir / "algorithm" / "index.json"),
        "memory_file": str(output_dir / "memory" / "leaves.json"),
        "logs_dir": str(output_dir / "logs"),
        "schema_dir": "io/input/schema",
        "features": {
            "slim_mode": True,
            "memory_recall": False,
            "embedding_split": False,
            "algorithm_catalog": False,
            "algorithm_registry_on_start": False,
            "tree_keep_history": False,
            "ollama_unload_after_request": True,
        },
        "growth": {
            "max_depth": 4,
            "max_loop_iters": 50,
            "max_expand_fail": 6,
            "max_expand_retry": 6,
            "max_frontier_per_iter": 16,
            "naming_use_llm": False,
            "similarity_threshold": 0.85,
            "parent_overlap_max": 0.92,
            "sibling_overlap_max": 0.95,
            "attach_on_invalid_split": True,
            "dedupe_siblings": True,
            "split_validation": "light",
        },
        "codegen": {
            "stub_on_fail": True,
            "compile_check": True,
            "require_all_branches": True,
            "max_retry": 6,
            "max_tree_passes": 10,
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
        "tests": {"enabled": True, "write_conftest": True},
    }
    return load_json(app_path, default_app)
