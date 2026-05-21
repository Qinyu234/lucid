# =========================
# FUNCTION: Semantic Layer
# PURPOSE:
# Maintain meaning of each node independent of LLM
# =========================

# =========================
# FUNCTION:
# update semantic
# =========================


def update_semantic(tree):

    root=tree["root"]

    queue=[root]

    while queue:

        node=queue.pop()

        if len(
            node.code
        )>200:

            node.semantic=(
                node.code[:100]
            )

        queue.extend(
            node.children
        )

def extract_semantic(code):
    # placeholder heuristic
    return "generated functionality"


def is_complete(node):
    # simple heuristic
    return len(node.code) > 200