from src.schema.io.io_in_names import io_in_names
from src.schema.io.io_out_names import io_out_names
from src.schema.io.io_type_map import io_type_map
from src.schema.io.normalize_io import normalize_io


def check_io_compatible(node: dict, candidate: dict) -> tuple:

    from src.config.load_app_config import load_app_config
    from src.schema.check_io_link import check_io_link

    mem = load_app_config().get("memory", {})
    require_out = mem.get("io_require_out_subset", True)
    require_in = mem.get("io_require_in_overlap", True)

    req = normalize_io(node.get("io"))
    cand = normalize_io(candidate.get("io"))

    req_out = set(io_out_names(req))
    cand_out = set(io_out_names(cand))
    req_in = set(io_in_names(req))
    cand_in = set(io_in_names(cand))

    if require_out and req_out and not req_out.issubset(cand_out):
        return False, f"output not covered: need {sorted(req_out)}, has {sorted(cand_out)}"

    if require_in and req_in:
        if not cand_in:
            return False, "candidate has no input keys"
        if not (req_in & cand_in) and not req_in.issubset(cand_in):
            return False, f"input incompatible: need {sorted(req_in)}, has {sorted(cand_in)}"

    for key in req_out & cand_out:
        rt = io_type_map(req, "out").get(key)
        ct = io_type_map(cand, "out").get(key)
        if rt and ct and rt != ct and rt != "any" and ct != "any":
            return False, f"output type mismatch on '{key}': {rt} vs {ct}"

    link_issues = check_io_link(req, cand, label="memory")
    if link_issues:
        return False, link_issues[0]

    return True, ""
