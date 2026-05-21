# =========================
# FUNCTION: Program Growth Runtime
# PURPOSE:
# Grow structure first, then fill implementation.
#
# LLM:
#   - expand project
#   - write code
#
# HOST:
#   - maintain tree
#   - semantic
#   - filesystem
# =========================

from .tree import (
    init_tree,
    is_converged
)

from .llm_interface import (
    expand_structure,
    traverse_and_fill
)

from .semantic import (
    update_semantic
)

from .analyzer import (
    find_undefined
)

from .growth import (
    add_nodes
)

from .fsmap import (
    sync_filesystem
)


def run(seed,llm,max_iters=30):

    tree=init_tree(seed)

    while True:

        tree["iteration"]+=1

        print(
            f"[ITER] {tree['iteration']}"
        )

        # phase1
        expand_structure(
            tree,
            llm
        )

        # phase2
        traverse_and_fill(
            tree,
            llm
        )

        update_semantic(
            tree
        )

        undefined=find_undefined(
            tree
        )

        if undefined:

            print(
                "undefined:",
                undefined
            )

            add_nodes(
                tree,
                undefined
            )

        sync_filesystem(
            tree
        )

        print(
            "children:",
            len(
                tree["root"].children
            )
        )

        if is_converged(
            tree
        ):

            print(
                "[DONE]"
            )

            break

        if tree["iteration"]>=max_iters:

            print(
                "[STOP]"
            )

            break

    return tree