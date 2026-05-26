def verify_generated_code(code: str, expected_fn: str, kind: str, child_modules: set | None=None, shared_root: str='shared', algorithm_root: str='algorithm') -> tuple:
    import ast
    from src.import_rules.verify_init_imports import verify_init_imports
    from src.import_rules.verify_leaf_imports import verify_leaf_imports
    from src.import_rules.verify_shared_imports import verify_shared_imports
    from src.import_rules.verify_single_named_function import verify_single_named_function
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return (False, str(e))
    ok, msg = verify_single_named_function(tree, expected_fn)
    if not ok:
        return (False, msg)
    if kind == 'leaf':
        return verify_leaf_imports(tree, shared_root, algorithm_root)
    if kind == 'init':
        return verify_init_imports(tree, child_modules or set(), shared_root, algorithm_root)
    if kind in ('shared', 'algorithm'):
        return verify_shared_imports(tree)
    return (False, f'unknown kind: {kind}')
