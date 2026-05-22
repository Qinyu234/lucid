from src.dataflow import check_seq_chain
from src.log import get_logger, log_event
from src.schema import validate_node

from .collect_growing_nodes import collect_growing_nodes
from .expand import expand
from .steps_to_nodes import steps_to_nodes
from .assign_topology import assign_topology
from .filter import filter, all_too_similar_to_parent
from .attach_children import attach_children


def growth_loop(root, job_id=None):

    logger = get_logger(job_id)
    iter_count = 0

    log_event(logger, "growth_loop_start", job_id=job_id)

    while True:

        log_event(logger, "growth_loop_iter", iter=iter_count)

        nodes = collect_growing_nodes(root)

        if len(nodes) == 0:
            log_event(logger, "growth_loop_converged", iter=iter_count)
            break

        for node in nodes:

            log_event(
                logger,
                "growth_expand_start",
                semantic=node.get("semantic"),
                function_name=node.get("function_name"),
            )

            expanded = expand(node, job_id=job_id)
            steps = expanded.get("steps", [])

            if not steps:
                fails = node.get("expand_fail", 0) + 1
                node["expand_fail"] = fails
                log_event(
                    logger,
                    "growth_expand_failed",
                    level=30,
                    expand_fail=fails,
                    semantic=node.get("semantic"),
                )
                if fails >= 5:
                    node["status"] = "done"
                    node["converge_reason"] = "expand_failed"
                continue

            node["expand_fail"] = 0

            raw_proposal = steps_to_nodes(steps)

            if all_too_similar_to_parent(raw_proposal, node.get("semantic")):
                node["status"] = "done"
                node["converge_reason"] = "similarity"
                log_event(logger, "growth_similarity_converged", reason="all_steps_similar_to_parent")
                continue

            topology = assign_topology(steps)
            proposal = filter(raw_proposal, parent_semantic=node.get("semantic"))

            if not proposal:
                node["status"] = "done"
                node["converge_reason"] = "similarity"
                log_event(logger, "growth_similarity_converged", reason="filter_empty")
                continue

            for child in proposal:
                child["status"] = "growing"
                vr, _ = validate_node(child)
                if not vr.ok:
                    log_event(logger, "growth_child_schema_warn", level=30, errors=vr.errors)

            attach_children(
                node,
                proposal,
                topology,
                boundary={"io": expanded.get("io")},
            )

            if topology == "SEQ":
                check_seq_chain(node["children"], job_id=job_id)

            if node.get("children"):
                node["status"] = "done"
                node["converge_reason"] = "expanded"
                vr, prepared = validate_node(node)
                if vr.ok:
                    node["io"] = prepared["io"]

                log_event(
                    logger,
                    "growth_node_expanded",
                    topology=topology,
                    children=len(node["children"]),
                )

        iter_count += 1
