def render_topology_templates(min_n: int = 2, max_n: int = 6, out_dir: str | None = None) -> dict:
    """
    Generate __init__ for every catalog template (unit-composed) per leaf count 2..6.

    Classification axis: leaf_count + template_id (not SEQ/PAR/ROUTER alone).
    """
    from src.shared.lib.path_write_text_util import path_write_text_util
    from src.pipeline.growth_loop.topology_catalog import topology_catalog
    from src.pipeline.code_tree.render_init import render_init

    def _fixture_children(count: int) -> list:
        children = []
        for i in range(count):
            children.append(
                {
                    "function_name": f"step_{i}",
                    "semantic": f"fixture leaf {i}",
                    "io": {"in": [], "out": []},
                    "children": [],
                    "case": f"CASE_{i}",
                    "tag": f"CASE_{i}",
                }
            )
        return children

    out: dict = {}
    lo = max(2, int(min_n))
    hi = max(lo, int(max_n))
    for entry in topology_catalog():
        n = entry["leaf_count"]
        if n < lo or n > hi:
            continue
        tid = entry["template_id"]
        node = {
            "function_name": f"fixture_{tid}",
            "semantic": f"template {tid} ({entry.get('units', '')})",
            "topology": entry.get("topology", "SEQ"),
            "template_id": tid,
            "topology_tree": entry["tree"],
            "io": {"in": [{"name": "input", "type": "str"}], "out": [{"name": "output", "type": "str"}]},
            "children": _fixture_children(n),
        }
        source = render_init(node)
        out[(n, tid)] = source
        if out_dir:
            path_write_text_util(f"{out_dir}/{n}_{tid}.init.py", source)
    return out
