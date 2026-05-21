from .tree import Node


def add_nodes(
    tree,
    undefined
):

    root=tree["root"]

    names=set()

    for c in root.children:

        names.add(
            c.name
        )

    undefined=undefined[:5]

    for name in undefined:

        if name in names:

            continue

        node=Node(
            name=name,
            semantic=name
        )

        root.add_child(
            node
        )

        print(
            "[NEW]",
            name
        )