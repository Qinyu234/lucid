def compile_module(path: str) -> tuple:
    import py_compile
    from pathlib import Path
    file_path = Path(path)
    if not file_path.exists():
        return (False, f'file not found: {path}')
    try:
        py_compile.compile(str(file_path), doraise=True)
    except py_compile.PyCompileError as exc:
        return (False, str(exc))
    return (True, '')
