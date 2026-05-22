from src.schema.io import normalize_io


def check_io_compatible(node: dict, candidate: dict) -> tuple:

    from src.config import load_app_config
    mem = load_app_config().get("memory", {})
    require_out = mem.get("io_require_out_subset", True)
    require_in = mem.get("io_require_in_overlap", True)

    req = normalize_io(node.get("io"))
    cand = normalize_io(candidate.get("io"))

    req_in, req_out = set(req["in"]), set(req["out"])
    cand_in, cand_out = set(cand["in"]), set(cand["out"])

    if require_out and req_out and not req_out.issubset(cand_out):
        return False, f"output not covered: need {sorted(req_out)}, has {sorted(cand_out)}"

    if require_in and req_in:
        if not cand_in:
            return False, "candidate has no input keys"
        if not (req_in & cand_in) and not req_in.issubset(cand_in):
            return False, f"input incompatible: need {sorted(req_in)}, has {sorted(cand_in)}"

    return True, ""
