from .collect_growing_nodes import collect_growing_nodes
from .ipo_to_node import ipo_to_nodes
from .expand import expand
from .filter import filter
from .attach_children import attach_children
from .update_status import update_status


def growth_loop(root):

    MAX_RETRY = 3

    while True:

        # =====================
        # 1. collect active nodes
        # =====================

        nodes = collect_growing_nodes(root)

        # =====================
        # convergence
        # =====================

        if len(nodes) == 0:
            break

        # =====================
        # 2. process nodes (NODE-DRIVEN)
        # =====================

        for node in nodes:

            # =====================
            # INPUT (node itself, no task layer)
            # =====================

            active_context = node.get("semantic")

            # =====================
            # TRANSFORM
            # =====================

            ipo = expand(node)

            proposal = ipo_to_nodes(ipo)

            accepted = filter(proposal)

            # =====================
            # retry mechanism
            # =====================

            if not accepted:

                node["retry"] = node.get("retry", 0) + 1

                if node["retry"] >= MAX_RETRY:
                    node["status"] = "done"

                continue

            # =====================
            # OUTPUT
            # =====================

            attach_children(node, proposal)

            update_status(node)