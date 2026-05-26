def seed(job):
    from src.shared.empty_io import empty_io
    return {'function_name': job['id'], 'semantic': job['goal'], 'children': [], 'topology': None, 'status': 'growing', 'role': 'composite', 'tag': None, 'case': None, 'io': empty_io(), 'code_path': job['root_path'], 'depth': 0, 'code_ok': None}
