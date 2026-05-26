def render_test(node: dict) -> str:
    from src.shared.format_io_comment import format_io_comment
    from src.shared.normalize_io import normalize_io
    from src.pipeline.code_tree.generate_test.sample_values import sample_values

    def _ctx_data_block(io_in: list) -> str:
        if not io_in:
            return ''
        lines = []
        for field in io_in:
            name = field['name']
            expr = sample_values(field.get('type', 'any'), name)
            lines.append(f'            "{name}": {expr},')
        return '\n'.join(lines)

    def _out_asserts(out_keys: list) -> str:
        if not out_keys:
            return '    # no io.out keys declared'
        return '\n'.join((f'    assert "{key}" in out["data"]' for key in out_keys))
    fn = node.get('function_name') or 'module'
    io = normalize_io(node.get('io'))
    io_in, io_out = format_io_comment(io)
    out_keys = [field['name'] for field in io.get('out', [])]
    return f'''# auto-generated test\n# semantic: {node.get('semantic', '')}\n# io.in: {io_in}\n# io.out: {io_out}\n\nimport importlib.util\nfrom pathlib import Path\n\n_MODULE_PATH = Path(__file__).resolve().parent / "{fn}.py"\n\n\ndef _load_module():\n    spec = importlib.util.spec_from_file_location("{fn}", _MODULE_PATH)\n    if spec is None or spec.loader is None:\n        raise ImportError(f"cannot load {{_MODULE_PATH}}")\n    mod = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(mod)\n    return mod\n\n\ndef test_{fn}_smoke():\n    mod = _load_module()\n    ctx = {{\n        "meta": {{}},\n        "state": {{}},\n        "data": {{\n{_ctx_data_block(io.get('in', []))}\n        }},\n        "error": None,\n    }}\n    out = mod.{fn}(ctx)\n    assert isinstance(out, dict)\n    assert "data" in out\n{_out_asserts(out_keys)}\n'''
