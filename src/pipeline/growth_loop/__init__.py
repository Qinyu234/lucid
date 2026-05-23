from src.config.load_app_config import load_app_config

from .collect_growing_nodes import collect_growing_nodes
from .expand import expand
from .steps_to_nodes import steps_to_nodes
from .assign_topology import assign_topology
from .filter.evaluate_split import evaluate_split
from .attach_children import attach_children
from .store_tree import store_tree


def growth_loop(root: dict, job_id: str | None = None, job: dict | None = None):

    from src.log.get_logger import get_logger
    from src.log.log_event import log_event

    def _growth_cfg() -> dict:
        return load_app_config().get("growth", {})

    def _mark_leaf(node, reason: str):
        node["status"] = "done"
        node["role"] = "leaf"
        node["converge_reason"] = reason

    def _mark_failed(node, reason: str = "expand_failed"):
        node["status"] = "failed"
        node["role"] = "leaf"
        node["converge_reason"] = reason

    def _snapshot(root: dict, job: dict | None, stage: str, job_id: str | None, **extra):
        growing = collect_growing_nodes(root)
        store_tree(
            root,
            job,
            stage,
            status="growing" if growing else "done",
            extra={
                "growing_count": len(growing),
                "growing_semantics": [n.get("semantic") for n in growing[:20]],
                **extra,
            },
            job_id=job_id,
        )

    logger = get_logger(job_id)
    cfg = _growth_cfg()

    max_depth = int(cfg.get("max_depth", 4))
    max_iters = int(cfg.get("max_loop_iters", 20))
    max_expand_fail = int(cfg.get("max_expand_fail", 3))
    max_frontier = int(cfg.get("max_frontier_per_iter", 8))

    iter_count = 0
    log_event(logger, "growth_loop_start", job_id=job_id, max_depth=max_depth)

    store_tree(root, job, "growth_start", status="growing", job_id=job_id)

    while iter_count < max_iters:

        log_event(logger, "growth_loop_iter", iter=iter_count)

        nodes = collect_growing_nodes(root)
        nodes.sort(key=lambda n: n.get("depth", 0))

        if len(nodes) == 0:
            log_event(logger, "growth_loop_converged", iter=iter_count)
            _snapshot(root, job, "growth_converged", job_id, iter=iter_count)
            break

        if len(nodes) > max_frontier:
            log_event(logger, "growth_frontier_trim", total=len(nodes), kept=max_frontier)
            nodes = nodes[:max_frontier]

        for node in nodes:

            depth = node.get("depth", 0)
            if depth >= max_depth:
                _mark_leaf(node, "max_depth")
                log_event(logger, "growth_max_depth", depth=depth, semantic=node.get("semantic"))
                continue

            log_event(
                logger,
                "growth_expand_start",
                depth=depth,
                semantic=node.get("semantic"),
                function_name=node.get("function_name"),
            )

            expanded = expand(node, job_id=job_id)
            steps = expanded.get("steps", [])

            if not steps:
                fails = node.get("expand_fail", 0) + 1
                node["expand_fail"] = fails
                log_event(logger, "growth_expand_failed", level=30, expand_fail=fails)
                if fails >= max_expand_fail:
                    _mark_failed(node)
                continue

            node["expand_fail"] = 0
            proposal = steps_to_nodes(steps, job_id=job_id)

            valid, reason, accepted = evaluate_split(node.get("semantic", ""), proposal)

            if not valid:
                _mark_leaf(node, "invalid_split")
                log_event(
                    logger,
                    "growth_invalid_split",
                    reason=reason,
                    semantic=node.get("semantic"),
                    step_count=len(proposal),
                )
                continue

            topology = assign_topology(accepted)

            for child in accepted:
                child["status"] = "growing"

            attach_children(
                node,
                accepted,
                topology,
                boundary={"io": expanded.get("io")},
            )

            if topology == "SEQ":
                from src.schema.check_seq_chain import check_seq_chain

                for msg in check_seq_chain(node["children"]):
                    log_event(logger, "growth_io_mismatch", level=30, error=msg)

            node["status"] = "done"
            node["role"] = "composite"
            node["converge_reason"] = "expanded"

            log_event(
                logger,
                "growth_node_expanded",
                topology=topology,
                children=len(accepted),
                depth=depth,
                split_reason=reason,
            )

        iter_count += 1
        _snapshot(root, job, f"growth_iter_{iter_count}", job_id, iter=iter_count)

    if iter_count >= max_iters:
        log_event(logger, "growth_loop_max_iters", level=30, max_iters=max_iters)
        _snapshot(root, job, "growth_max_iters", job_id, iter=iter_count)

    store_tree(
        root,
        job,
        "growth_loop_end",
        extra={"iterations": iter_count},
        job_id=job_id,
    )
