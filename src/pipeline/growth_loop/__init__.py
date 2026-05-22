from .collect_growing_nodes import collect_growing_nodes
from .expand import expand
from .ipo_to_nodes import ipo_to_nodes
from .filter import filter
from .attach_children import attach_children


def growth_loop(root):

    MAX_RETRY = 3

    iter_count = 0

    while True:

        print("\n===== LOOP =====")

        print(
            "ITER:",
            iter_count
        )

        # =====================
        # collect active nodes
        # =====================

        nodes = collect_growing_nodes(
            root
        )

        print("GROWING:")

        print([
            x.get("semantic")
            for x in nodes
        ])

        # =====================
        # convergence
        # =====================

        if len(nodes) == 0:

            print(
                "NO ACTIVE NODES"
            )

            break

        # =====================
        # process nodes
        # =====================

        for node in nodes:

            print("\nNODE:")

            print(
                node["semantic"]
            )

            # =====================
            # EXPAND
            # =====================

            ipo = expand(node)

            print("IPO:")

            print(ipo)

            # =====================
            # IPO → NODE
            # =====================

            proposal = ipo_to_nodes(
                ipo
            )

            # =====================
            # FILTER
            # =====================

            proposal = filter(
                proposal
            )

            print("PROPOSAL:")

            print(proposal)

            accepted = (
                len(proposal) > 0
            )

            print(
                "ACCEPTED:",
                accepted
            )

            # =====================
            # retry
            # =====================

            if not accepted:

                node["retry"] = (
                    node.get(
                        "retry",
                        0
                    ) + 1
                )

                print(
                    "RETRY:",
                    node["retry"]
                )

                # =====================
                # convergence fallback
                # =====================

                if (
                    node["retry"]
                    >= MAX_RETRY
                ):

                    node[
                        "status"
                    ] = "done"

                continue

            # =====================
            # normalize child state
            # =====================

            for child in proposal:

                child[
                    "status"
                ] = "growing"

            # =====================
            # attach children
            # =====================

            attach_children(
                node,
                proposal
            )

            # =====================
            # current node complete
            #
            # children take over
            # =====================

            if node.get(
                "children"
            ):

                node[
                    "status"
                ] = "done"

        iter_count += 1