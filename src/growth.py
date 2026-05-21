# =========================
# FUNCTION:
# grow tree
# =========================

from .tree import Node


def add_nodes(
    tree,
    undefined
):

    root=tree["root"]

    undefined=undefined[:5]

    for name in undefined:

        node=Node(
            name=name,
            semantic=f"{name} function"
        )

        root.add_child(
            node
        )