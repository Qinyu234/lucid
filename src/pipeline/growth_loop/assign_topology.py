# =========================
# SYSTEM: topology assignment
# LLM proposes steps only; structure is decided here.
# =========================

ROUTER_MIN_BRANCHES = 2
MAX_CHILDREN = 4


def _distinct_case_tags(steps: list) -> list:
    tags = []
    for step in steps:
        if not isinstance(step, dict):
            continue
        tag = step.get("tag")
        if tag is None or tag == "":
            continue
        tags.append(str(tag).strip())
    return tags


def build_case_map(steps: list) -> dict:
    """
    Map semantic case tags to CASE_0, CASE_1, ...
    """
    tags = _distinct_case_tags(steps)
    unique = sorted(set(tags))
    return {tag: f"CASE_{i}" for i, tag in enumerate(unique)}


def assign_topology(steps: list) -> str:
    """
    v0.2: SEQ default
    v0.3: ROUTER when >=2 distinct case tags on steps
    PAR: not enabled yet
    """
    if not steps:
        return "SEQ"

    tags = _distinct_case_tags(steps)
    unique = set(tags)

    if len(unique) >= ROUTER_MIN_BRANCHES and len(tags) >= len(steps):
        # every step tagged and tags are pairwise distinct
        return "ROUTER"

    return "SEQ"
