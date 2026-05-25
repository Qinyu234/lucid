from src.algorithm.match_fixed_task import match_fixed_task


def format_algorithm_catalog(node: dict | None = None, limit: int = 6) -> str:
    entries = match_fixed_task(node, limit=limit) if node else []
    if not entries:
        from src.algorithm.list_algorithms import list_algorithms
        entries = list_algorithms(limit=limit)

    lines = [
        "Algorithms below are ONLY valid under fixed distribution + fixed business logic.",
        "Use one only when the current node matches the fixed_task regime.",
        "",
    ]

    for entry in entries:
        fn = entry.get("function_name", "")
        cat = entry.get("category", "")
        sem = entry.get("semantic", "")
        module = entry.get("module", f"algorithm.{fn}")
        fixed = entry.get("fixed_task") or {}
        adv = entry.get("relative_advantage") or {}

        lines.append(f"- {fn} [{cat}] import: from {module} import {fn}")
        lines.append(f"  semantic: {sem}")
        lines.append(f"  fixed.profile: {fixed.get('profile_id', '')}")
        lines.append(f"  fixed.distribution: {fixed.get('distribution', '')}")
        lines.append(f"  fixed.business: {fixed.get('business', '')}")
        lines.append(
            f"  relative_advantage: {adv.get('metric', '')} vs {adv.get('baseline', '')}"
        )
        if adv.get("margin"):
            lines.append(f"  margin (fixed regime): {adv.get('margin')}")

    return "\n".join(lines) if len(lines) > 3 else "- (no fixed-task algorithms registered)"
