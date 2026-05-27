def dedupe_sibling_names(children: list) -> list:
    from src.shared.lib.dedupe_sibling_names_util import dedupe_sibling_names_util

    return dedupe_sibling_names_util(children)
