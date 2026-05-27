def build_case_map(steps: list) -> dict:

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

    tags = _distinct_case_tags(steps)
    unique = sorted(set(tags))
    return {tag: f"CASE_{i}" for i, tag in enumerate(unique)}
