# =========================
# FUNCTION:
# collect_growing_nodes
#
# PURPOSE:
# traverse tree
# collect active nodes
#
# RULE:
# only collect:
# status=="growing"
# =========================


def collect_growing_nodes(node):

    nodes = []

    # =====================
    # current node
    # =====================

    if node["status"] == "growing":

        nodes.append(
            node
        )

    # =====================
    # children
    # =====================

    for child in node["children"]:

        child_nodes = (

            collect_growing_nodes(
                child
            )

        )

        nodes.extend(
            child_nodes
        )

    return nodes