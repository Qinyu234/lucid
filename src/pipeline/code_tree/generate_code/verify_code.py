import ast
import os


def verify_code(code, node):

    # =========================
    # 1. parse check
    # =========================
    try:
        tree = ast.parse(code)
    except:
        return False

    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]

    # must be exactly one function
    if len(funcs) != 1:
        return False

    func = funcs[0]
    func_name = func.name

    path = node["code_path"]
    children = node.get("children", [])

    file_name = os.path.basename(path)
    folder_name = os.path.basename(os.path.dirname(path))

    # =========================
    # 2. INTERFACE NODE (__init__.py)
    # =========================
    if children:

        # file must be __init__.py
        if file_name != "__init__.py":
            return False

        # function must be __init__
        if func_name != "__init__":
            return False

        # folder name must match semantic-derived name (soft rule optional)
        return True

    # =========================
    # 3. LEAF NODE (.py file)
    # =========================

    expected_func = node["semantic"][:40].strip().replace(" ", "_")

    expected_file = file_name.replace(".py", "")

    # function name must match file name
    if func_name != expected_file:
        return False

    # file name must match semantic-derived name
    if expected_func and expected_func != expected_file:
        return False

    return True