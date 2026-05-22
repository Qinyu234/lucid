from .generate_code import generate_code
from .write_file import write_file


def code_tree(root):

    stack = [(root, "")]

    while stack:

        node, base_path = stack.pop()

        # =========================
        # build path
        # =========================
        name = node["semantic"][:40].strip().replace(" ", "_")
        if not name:
            name = "unnamed_function"

        path = f"{base_path}/{name}" if base_path else name

        node["code_path"] = path

        children = node.get("children", [])

        # =========================
        # BRANCH NODE → __init__.py
        # =========================
        if children:

            code = generate_code(node)
            write_file(f"{path}/__init__.py", code)

            # push children
            for child in children:
                stack.append((child, path))

            continue

        # =========================
        # LEAF NODE → .py file
        # =========================
        code = generate_code(node)
        write_file(f"{path}.py", code)