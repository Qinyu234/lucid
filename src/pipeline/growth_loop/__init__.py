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
from .topology_catalog import topology_catalog


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

    def _tree_needs_seq_io_repair(tree) -> bool:
        if not isinstance(tree, dict):
            return True
        op = str(tree.get("op", "SEQ")).upper()
        if op in ("PAR", "ROUTER"):
            return False
        for arg in tree.get("args") or []:
            if isinstance(arg, dict) and not _tree_needs_seq_io_repair(arg):
                return False
        return True

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
            split_strategy = str(cfg.get("split_count_strategy", "estimate")).strip().lower()
            if split_strategy == "probe":
                from .probe_split_count import probe_split_count

                expanded = probe_split_count(node, job_id=job_id)
            else:
                from .estimate_split_count import estimate_split_count

                target = estimate_split_count(node.get("semantic", ""), cfg, depth=depth)
                expanded = expand(node, job_id=job_id, target_steps=target)
                event_util(
                    logger,
                    "growth_split_target",
                    strategy=split_strategy,
                    target_steps=target,
                    semantic=node.get("semantic", "")[:120],
                )
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
            split_result = evaluate_split_bridge(node.get("semantic", ""), proposal)
            valid = split_result[0]
            reason = split_result[1]
            accepted = split_result[2]
            split_analysis = split_result[3] if len(split_result) > 3 else {}
            if _growth_cfg().get("split_analysis", {}).get("embed_log", True):
                embed = split_analysis.get("embed_log") if isinstance(split_analysis, dict) else ""
                if embed:
                    logger.info("%s", embed)
            event_util(
                logger,
                "growth_split_analysis",
                valid=valid,
                reason=reason,
                step_count=len(proposal),
                accepted_count=len(accepted) if accepted else 0,
                topology_scores=(split_analysis or {}).get("topology_scores"),
                recommended_topology=(split_analysis or {}).get("recommended_topology"),
                recommended_template_id=(split_analysis or {}).get("recommended_template_id"),
                keep_split=(split_analysis or {}).get("keep_split"),
                plausibility=(split_analysis or {}).get("plausibility"),
                max_sibling_jaccard=(split_analysis or {}).get("max_sibling_jaccard"),
                seq_chain_score=(split_analysis or {}).get("seq_chain_score"),
                embed_log=(split_analysis or {}).get("embed_log") if _growth_cfg().get("split_analysis", {}).get("embed_json", False) else None,
            )
            if not valid:
                cfg_attach = _growth_cfg().get("attach_on_invalid_split", True)
                # Proactively reduce complexity: try fewer steps before giving up.
                # This is triggered by analysis_reject / io_out_collision and similar reasons.
                if not cfg_attach:
                    max_children = int(cfg.get("max_children", 6))
                    cur = min(max_children, len(steps))
                    while cur > int(cfg.get("min_children", 2)):
                        cur -= 1
                        event_util(
                            logger,
                            "growth_reduce_split_complexity",
                            level=30,
                            from_steps=len(steps),
                            to_steps=cur,
                            reason=reason,
                            function_name=node.get("function_name"),
                        )
                        expanded2 = expand(node, job_id=job_id, target_steps=cur)
                        steps2 = expanded2.get("steps", [])
                        if not steps2:
                            continue
                        proposal2 = steps_to_nodes(steps2, job_id=job_id)
                        split2 = evaluate_split_bridge(node.get("semantic", ""), proposal2)
                        if split2 and split2[0] and split2[2]:
                            valid = split2[0]
                            reason = split2[1]
                            accepted = split2[2]
                            split_analysis = split2[3] if len(split2) > 3 else {}
                            expanded = expanded2
                            steps = steps2
                            break
                if cfg_attach and proposal:
                    max_children = int(cfg.get("max_children", 6))
                    accepted = dedupe_sibling_names(proposal[:max_children])
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
            assignment = assign_topology(accepted, split_analysis)
            topology = assignment.get("topology") or "SEQ"
            for child in accepted:
                child["status"] = "growing"
            attach_children(node, accepted, assignment, boundary={"io": expanded.get("io")})
            if _tree_needs_seq_io_repair(assignment.get("tree")):
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
                template_id=assignment.get("template_id"),
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
                template_id=assignment.get("template_id"),
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
