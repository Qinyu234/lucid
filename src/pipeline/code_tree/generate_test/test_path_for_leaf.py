def test_path_for_leaf(code_path: str, function_name: str) -> str:
    from pathlib import Path

    _TEST_PREFIX = "test_"
    base = Path((code_path or function_name).replace("\\", "/"))
    fn = function_name or base.name or "module"
    return str(base.parent / f"{_TEST_PREFIX}{fn}.py").replace("\\", "/")
