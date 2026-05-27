def render_test(node: dict) -> str:
    from src.shared.validate.io_format_comment_util import io_format_comment_util
    from src.shared.validate.io_normalize_util import io_normalize_util

    from .sample_values import sample_values

    def _ctx_data_block(io_in: list) -> str:
        if not io_in:
            return ""
        lines = []
        for field in io_in:
            name = field["name"]
            expr = sample_values(field.get("type", "any"), name)
            lines.append(f'            "{name}": {expr},')
        return "\n".join(lines)

    def _out_asserts(out_keys: list) -> str:
        if not out_keys:
            return "    # no io.out keys declared"
        return "\n".join((f'    assert "{key}" in out["data"]' for key in out_keys))

    fn = node.get("function_name") or "module"
    io = io_normalize_util(node.get("io"))
    io_in, io_out = io_format_comment_util(io)
    out_keys = [field["name"] for field in io.get("out", [])]
    return f'''# auto-generated test
# semantic: {node.get('semantic', '')}
# io.in: {io_in}
# io.out: {io_out}

import importlib.util
from pathlib import Path

_MODULE_PATH = Path(__file__).resolve().parent / "{fn}.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("{fn}", _MODULE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {{_MODULE_PATH}}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_{fn}_smoke():
    mod = _load_module()
    ctx = {{
        "meta": {{}},
        "state": {{}},
        "data": {{
{_ctx_data_block(io.get('in', []))}
        }},
        "error": None,
    }}
    out = mod.{fn}(ctx)
    assert isinstance(out, dict)
    assert "data" in out
{_out_asserts(out_keys)}
'''
