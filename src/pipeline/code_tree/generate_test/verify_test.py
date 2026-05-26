def verify_test(code: str, function_name: str) -> tuple:
    import ast
    expected = f'test_{function_name}_smoke'
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return (False, str(exc))
    tests = [node.name for node in tree.body if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')]
    if expected not in tests:
        return (False, f'missing test function {expected}')
    return (True, '')
