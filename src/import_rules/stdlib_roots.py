def stdlib_roots() -> set:
    import sys
    if hasattr(sys, 'stdlib_module_names'):
        return set(sys.stdlib_module_names)
    return {'os', 'sys', 'json', 're', 'math', 'time', 'pathlib', 'typing', 'collections', 'itertools', 'functools', 'datetime', 'logging', 'subprocess', 'copy', 'hashlib', 'base64', 'io', 'abc', 'ast'}
