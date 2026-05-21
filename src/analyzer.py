import ast


def find_undefined(tree):

    undefined=[]

    root=tree["root"]

    queue=[root]

    while queue:

        node=queue.pop()

        try:

            t=ast.parse(
                node.code
            )

        except:

            queue.extend(
                node.children
            )

            continue

        funcs=set()

        called=set()

        for n in ast.walk(t):

            if isinstance(
                n,
                ast.FunctionDef
            ):

                funcs.add(
                    n.name
                )

            elif isinstance(
                n,
                ast.Call
            ):

                if isinstance(
                    n.func,
                    ast.Name
                ):

                    called.add(
                        n.func.id
                    )

        for c in called:

            if c not in funcs:

                undefined.append(
                    c
                )

        queue.extend(
            node.children
        )

    return list(
        set(undefined)
    )

    undefined=[]

    root=tree["root"]

    queue=[root]

    while queue:

        node=queue.pop()

        try:

            t=ast.parse(
                node.code
            )

        except:

            queue.extend(
                node.children
            )

            continue

        funcs=set()

        called=set()

        for n in ast.walk(t):

            if isinstance(
                n,
                ast.FunctionDef
            ):

                funcs.add(
                    n.name
                )

            elif isinstance(
                n,
                ast.Call
            ):

                if hasattr(
                    n.func,
                    "id"
                ):

                    called.add(
                        n.func.id
                    )

        for c in called:

            if c not in funcs:

                undefined.append(
                    c
                )

        queue.extend(
            node.children
        )

    return list(
        set(undefined)
    )