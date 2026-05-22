from .generate_code import generate_code
from .write_file import write_file


def code_tree(root):

    stack = [root]

    while stack:

        node = stack.pop()

        children = node.get(
            "children",
            []
        )

        path = node[
            "code_path"
        ]

        # =========================
        # BRANCH NODE
        # =========================

        if children:

            code = generate_code(
                node
            )

            write_file(
                f"{path}/__init__.py",
                code
            )

            # =========================
            # propagate children path
            # =========================

            for child in children:

                fn = child.get(
                    "function_name"
                )

                if not fn:

                    fn = "unnamed"

                child[
                    "code_path"
                ] = (
                    f"{path}/{fn}"
                )

                stack.append(
                    child
                )

            continue

        # =========================
        # LEAF NODE
        # =========================

        code = generate_code(
            node
        )

        write_file(
            f"{path}.py",
            code
        )