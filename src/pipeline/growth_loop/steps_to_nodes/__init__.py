from .generate_function_name import generate_function_name

def steps_to_nodes(steps: list, job_id=None) -> list:
    from ..build_case_map import build_case_map
    from src.shared.normalize_io import normalize_io
    case_map = build_case_map(steps)
    children = []
    used_names: set[str] = set()
    for step in steps:
        semantic = step['semantic']
        node = {'semantic': semantic, 'function_name': None, 'children': [], 'status': 'growing', 'role': 'leaf', 'code_path': None, 'topology': None, 'tag': step.get('tag'), 'case': None, 'io': normalize_io(step.get('io')), 'code_ok': None}
        if step.get('tag') and case_map:
            node['case'] = case_map.get(step['tag'])
        node['function_name'] = generate_function_name(node, job_id=job_id, used_names=used_names)
        used_names.add(node['function_name'])
        children.append(node)
    return children
