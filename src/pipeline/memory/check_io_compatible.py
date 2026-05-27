def check_io_compatible(node: dict, candidate: dict) -> tuple:
    from src.shared.validate.io_in_names_util import io_in_names_util
    from src.shared.validate.io_out_names_util import io_out_names_util
    from src.shared.validate.io_type_map_util import io_type_map_util
    from src.shared.validate.io_normalize_util import io_normalize_util
    from src.shared.lib.app_config_util import app_config_util
    from src.shared.validate.io_link_util import io_link_util
    mem = app_config_util().get('memory', {})
    require_out = mem.get('io_require_out_subset', True)
    require_in = mem.get('io_require_in_overlap', True)
    req = io_normalize_util(node.get('io'))
    cand = io_normalize_util(candidate.get('io'))
    req_out = set(io_out_names_util(req))
    cand_out = set(io_out_names_util(cand))
    req_in = set(io_in_names_util(req))
    cand_in = set(io_in_names_util(cand))
    if require_out and req_out and (not req_out.issubset(cand_out)):
        return (False, f'output not covered: need {sorted(req_out)}, has {sorted(cand_out)}')
    if require_in and req_in:
        if not cand_in:
            return (False, 'candidate has no input keys')
        if not req_in & cand_in and (not req_in.issubset(cand_in)):
            return (False, f'input incompatible: need {sorted(req_in)}, has {sorted(cand_in)}')
    for key in req_out & cand_out:
        rt = io_type_map_util(req, 'out').get(key)
        ct = io_type_map_util(cand, 'out').get(key)
        if rt and ct and (rt != ct) and (rt != 'any') and (ct != 'any'):
            return (False, f"output type mismatch on '{key}': {rt} vs {ct}")
    link_issues = io_link_util(req, cand, label='memory')
    if link_issues:
        return (False, link_issues[0])
    return (True, '')
