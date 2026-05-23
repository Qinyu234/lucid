# SYSTEM: topology assignment after valid LLM split

ROUTER_MIN_BRANCHES = 2
MAX_CHILDREN = 4


def assign_topology(steps: list) -> str:
    """
    Called only after split passed similarity validation.
    SEQ | PAR | ROUTER
    """

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

    def _has_parallel_tag(steps: list) -> bool:
        for step in steps:
            tag = (step.get("tag") or "").lower()
            if tag in ("parallel", "par"):
                return True
        return False

    if not steps:
        return "SEQ"

    tags = _distinct_case_tags(steps)
    unique = set(tags)

    if len(unique) >= ROUTER_MIN_BRANCHES and len(tags) >= len(steps):
        return "ROUTER"

    if _has_parallel_tag(steps):
        return "PAR"

    return "SEQ"
