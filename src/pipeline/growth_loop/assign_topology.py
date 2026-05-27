def assign_topology(steps: list, analysis: dict | None = None) -> dict:
    """
    Pick composite template from unit-composed catalog.

    When analysis is present (from evaluate_split), use recommended_template_id
    and topology_scores (SEQ / PAR / ROUTER).
    """
    from src.shared.lib.app_config_util import app_config_util
    from src.pipeline.growth_loop.topology_catalog import topology_catalog

    n = sum(1 for step in steps if isinstance(step, dict))
    if n <= 1:
        return {
            "template_id": "seq_1",
            "tree": {"op": "SEQ", "args": [0] if n == 1 else []},
            "topology": "SEQ",
        }

    tid = None
    if isinstance(analysis, dict):
        tid = analysis.get("recommended_template_id")
    if tid:
        entry = topology_catalog(template_id=tid)
        if entry and entry.get("leaf_count") == n:
            return {
                "template_id": entry["template_id"],
                "tree": entry["tree"],
                "topology": entry.get("topology") or entry["tree"].get("op", "SEQ"),
                "topology_scores": (analysis or {}).get("topology_scores"),
            }

    _DEFAULT_ID = {2: "par_2", 3: "seq1_par_2", 4: "seq_4", 5: "seq_5", 6: "seq_6"}
    cfg = app_config_util().get("growth", {}).get("template_by_count") or {}
    tid = cfg.get(n) or cfg.get(str(n)) or _DEFAULT_ID.get(n)
    entry = topology_catalog(template_id=tid) if tid else None
    if not entry:
        options = topology_catalog(leaf_count=n)
        entry = (
            options[0]
            if options
            else {"template_id": f"seq_{n}", "tree": {"op": "SEQ", "args": list(range(n))}, "topology": "SEQ"}
        )
    out = {
        "template_id": entry["template_id"],
        "tree": entry["tree"],
        "topology": entry.get("topology") or entry["tree"].get("op", "SEQ"),
    }
    if isinstance(analysis, dict) and analysis.get("topology_scores"):
        out["topology_scores"] = analysis["topology_scores"]
    return out
