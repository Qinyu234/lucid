def py_compile_util(path: str) -> tuple:
    import py_compile

    try:
        py_compile.compile(path, doraise=True)
        return True, ""
    except Exception as e:
        return False, str(e)
