def probe_split_count(node: dict, job_id: str | None = None) -> dict:
    """
    Try expand from min_children upward until split validation accepts a proposal.

    Costs up to (max_children - min_children + 1) LLM expand calls; use when
    estimate_split_count is unreliable. Prefer estimate_split_count for speed.
    """
    from src.shared.lib.app_config_util import app_config_util
    from src.shared.validate.io_empty_util import io_empty_util

    from src.pipeline.growth_loop.expand import expand
    from src.pipeline.growth_loop.filter import evaluate_split
    from src.pipeline.growth_loop.steps_to_nodes import steps_to_nodes

    cfg = app_config_util().get("growth", {})
    min_n = int(cfg.get("min_children", 2))
    max_n = int(cfg.get("max_children", 6))
    empty = {"steps": [], "io": io_empty_util()}
    semantic = node.get("semantic", "")
    for target in range(min_n, max_n + 1):
        expanded = expand(node, job_id=job_id, target_steps=target)
        steps = expanded.get("steps") or []
        if len(steps) < min_n:
            continue
        proposal = steps_to_nodes(steps, job_id=job_id)
        split_result = evaluate_split(semantic, proposal)
        valid = split_result[0]
        accepted = split_result[2]
        if valid and accepted:
            trimmed = accepted[:max_n]
            return {"steps": steps[: len(trimmed)], "io": expanded.get("io") or io_empty_util()}
    return empty
