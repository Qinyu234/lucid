def dedupe_sibling_names_util(children: list) -> list:
    used: set[str] = set()
    for child in children:
        fn = child.get("function_name") or "unnamed"
        base = fn
        if fn in used:
            idx = 2
            while f"{base}_{idx}" in used:
                idx += 1
            fn = f"{base}_{idx}"
            child["function_name"] = fn
        used.add(fn)
    return children
