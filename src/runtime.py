# =========================
# FUNCTION: Program Growth Runtime
# PURPOSE:
# Expand project from src/main.py
# using iterative local generation.
#
# LLM:
#   - write code
#   - split structure
#
# HOST:
#   - maintain tree
#   - semantic storage
#   - filesystem sync
#   - convergence
# =========================

from .tree import (
    init_tree,
    is_converged
)

from .llm_interface import (
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


def run(seed,llm,max_iters=50):

    tree=init_tree(seed)

    tree["iteration"]=0

    while True:

        tree["iteration"]+=1

        print(
            f"[ITER] {tree['iteration']}"
        )

        # LLM扩展当前活跃节点
        traverse_and_fill(
            tree,
            llm
        )

        # 更新semantic
        update_semantic(
            tree
        )

        # 从代码分析缺失函数
        undefined=find_undefined(
            tree
        )

        # 基于undefined扩展tree
        if undefined:

            add_nodes(
                tree,
                undefined
            )

        # 同步到staging
        sync_filesystem(
            tree
        )

        # 收敛
        if is_converged(tree):

            print(
                "[DONE]"
            )

            break

        if tree["iteration"]>=max_iters:

            print(
                "[STOP] iteration limit"
            )

            break

    return tree