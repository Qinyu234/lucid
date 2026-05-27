from .assign_topology import assign_topology
from .attach_children import attach_children
from .collect_growing_nodes import collect_growing_nodes
from .dedupe_sibling_names import dedupe_sibling_names
from .evaluate_split_bridge import evaluate_split_bridge
from .expand import expand
from .filter import filter
from .seq_io_repair import seq_io_repair
from .shared_ctx import shared_ctx
from .steps_to_nodes import steps_to_nodes
from .store_tree import store_tree


def growth_loop(root: dict, job_id: str | None = None, job: dict | None = None):
    ctx = shared_ctx({"data": {}, "meta": {}, "state": {}, "error": None})
    get_logger_util = ctx["meta"]["get_logger_util"]
    app_config_util = ctx["meta"]["app_config_util"]
    event_util = ctx["meta"]["event_util"]
    seq_ctx = seq_io_repair({"data": {}, "meta": {}, "state": {}, "error": None})
    io_seq_chain_util = seq_ctx["meta"]["io_seq_chain_util"]
    io_repair_seq_util = seq_ctx["meta"]["io_repair_seq_util"]

    def _growth_cfg() -> dict:
        return app_config_util().get("growth", {})

    def _mark_leaf(node, reason: str):
        node["status"] = "done"
        node["role"] = "leaf"
        node["converge_reason"] = reason

    def _mark_failed(node, reason: str = "expand_failed"):
        _mark_leaf(node, reason)

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

    logger = get_logger_util(job_id)
    cfg = _growth_cfg()
    max_depth = int(cfg.get("max_depth", 4))
    max_iters = int(cfg.get("max_loop_iters", 50))
    max_expand_fail = int(cfg.get("max_expand_fail", 6))
    max_frontier = int(cfg.get("max_frontier_per_iter", 8))
    iter_count = 0
    event_util(logger, "growth_loop_start", job_id=job_id, max_depth=max_depth)
    store_tree(root, job, "growth_start", status="growing", job_id=job_id)
    while True:
        nodes = collect_growing_nodes(root)
        if not nodes:
            event_util(logger, "growth_loop_converged", iter=iter_count)
            _snapshot(root, job, "growth_converged", job_id, iter=iter_count)
            break
        if iter_count >= max_iters:
            event_util(logger, "growth_loop_max_iters", level=30, max_iters=max_iters, growing=len(nodes))
            _snapshot(root, job, "growth_max_iters", job_id, iter=iter_count, growing=len(nodes))
            break
        event_util(logger, "growth_loop_iter", iter=iter_count)
        nodes.sort(key=lambda n: n.get("depth", 0))
        if len(nodes) > max_frontier:
            event_util(logger, "growth_frontier_trim", total=len(nodes), kept=max_frontier)
            nodes = nodes[:max_frontier]
        for node in nodes:
            depth = node.get("depth", 0)
            if depth >= max_depth:
                _mark_leaf(node, "max_depth")
                event_util(logger, "growth_max_depth", depth=depth, semantic=node.get("semantic"))
                _snapshot(
                    root,
                    job,
                    f"growth_max_depth_{node.get('function_name', 'node')}",
                    job_id,
                    function_name=node.get("function_name"),
                )
                continue
            event_util(
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
                event_util(logger, "growth_expand_failed", level=30, expand_fail=fails)
                if fails >= max_expand_fail:
                    _mark_failed(node)
                    _snapshot(
                        root,
                        job,
                        f"growth_expand_failed_{node.get('function_name', 'node')}",
                        job_id,
                        function_name=node.get("function_name"),
                        expand_fail=fails,
                    )
                continue
            node["expand_fail"] = 0
            proposal = steps_to_nodes(steps, job_id=job_id)
            valid, reason, accepted = evaluate_split_bridge(node.get("semantic", ""), proposal)
            if not valid:
                cfg_attach = _growth_cfg().get("attach_on_invalid_split", True)
                if cfg_attach and proposal:
                    accepted = dedupe_sibling_names(proposal[:4])
                    event_util(
                        logger,
                        "growth_weak_split",
                        level=30,
                        reason=reason,
                        attached=len(accepted),
                        semantic=node.get("semantic"),
                    )
                else:
                    _mark_leaf(node, "invalid_split")
                    event_util(
                        logger,
                        "growth_invalid_split",
                        reason=reason,
                        semantic=node.get("semantic"),
                        step_count=len(proposal),
                    )
                    _snapshot(
                        root,
                        job,
                        f"growth_invalid_split_{node.get('function_name', 'node')}",
                        job_id,
                        function_name=node.get("function_name"),
                        reason=reason,
                    )
                    continue
            if not accepted:
                _mark_leaf(node, "invalid_split")
                _snapshot(
                    root,
                    job,
                    f"growth_invalid_split_{node.get('function_name', 'node')}",
                    job_id,
                    function_name=node.get("function_name"),
                )
                continue
            topology = assign_topology(accepted)
            for child in accepted:
                child["status"] = "growing"
            attach_children(node, accepted, topology, boundary={"io": expanded.get("io")})
            if topology == "SEQ":
                repaired = io_repair_seq_util(node["children"])
                if repaired:
                    event_util(
                        logger,
                        "growth_io_repaired",
                        repairs=repaired[:10],
                        repair_count=len(repaired),
                    )
                for msg in io_seq_chain_util(node["children"]):
                    event_util(logger, "growth_io_mismatch", level=30, error=msg)
            node["status"] = "done"
            node["role"] = "composite"
            node["converge_reason"] = "expanded"
            event_util(
                logger,
                "growth_node_expanded",
                topology=topology,
                children=len(accepted),
                depth=depth,
                split_reason=reason,
            )
            _snapshot(
                root,
                job,
                f"growth_expanded_{node.get('function_name', 'node')}",
                job_id,
                function_name=node.get("function_name"),
                topology=topology,
                children=len(accepted),
                depth=depth,
            )
        iter_count += 1
        _snapshot(root, job, f"growth_iter_{iter_count}", job_id, iter=iter_count)
    remaining = collect_growing_nodes(root)
    for node in remaining:
        _mark_leaf(node, "growth_incomplete")
        event_util(
            logger,
            "growth_leftover_leaf",
            level=30,
            semantic=node.get("semantic"),
            function_name=node.get("function_name"),
        )
    store_tree(
        root,
        job,
        "growth_loop_end",
        extra={"iterations": iter_count, "leftover": len(remaining)},
        job_id=job_id,
    )
