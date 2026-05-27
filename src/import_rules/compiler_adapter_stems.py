"""Single-function compiler modules allowed to import non-shared inside the function body.

These are NOT user-project leaves; parent __init__.py imports them via from .<stem> import <stem>.
User-generated code must not add adapter modules.
"""

COMPILER_ADAPTER_STEMS = frozenset(
    {
        "shared_ctx",
        "invoke_llm",
        "extract_json",
        "persist_leaf",
        "leaf_stub",
        "recall_code",
        "render_reuse",
        "conftest_setup",
        "verify_generated",
        "write_leaf_test_bridge",
        "format_io_bridge",
        "normalize_io_bridge",
        "evaluate_split_bridge",
        "seq_io_repair",
        "format_runtime_error",
        "runtime_logging",
    }
)


def is_compiler_adapter_stem(stem: str) -> bool:
    if stem in COMPILER_ADAPTER_STEMS:
        return True
    return stem.endswith("_bridge")
