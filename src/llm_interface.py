from .llm import generate


def expand_structure(
    tree,
    llm
):

    root=tree["root"]

    if root.children:

        return

    prompt=f"""
goal:

{root.semantic}

Create helper functions.

Output only python skeleton.

Example:

def capture():
    pass
"""

    code=generate(
        prompt
    )

    root.code+=(
        "\n"+code
    )


def traverse_and_fill(
    tree,
    llm
):

    nodes=collect_active_nodes(
        tree
    )

    for node in nodes:

        prompt=build_prompt(
            node
        )

        code=generate(
            prompt
        )

        node.update_code(
            node.code+
            "\n"+
            code
        )


def collect_active_nodes(
    tree
):

    nodes=[]

    q=[tree["root"]]

    while q:

        n=q.pop()

        if not n.completed:

            nodes.append(
                n
            )

        q.extend(
            n.children
        )

    return nodes


def build_prompt(
    node
):

    return f"""
semantic:

{node.semantic}

existing code:

{node.code}

Implement code.

Only output code.
"""