def seed(job):
    from src.shared.validate.io_empty_util import io_empty_util
    return {'function_name': job['id'], 'semantic': job['goal'], 'children': [], 'topology': None, 'status': 'growing', 'role': 'composite', 'tag': None, 'case': None, 'io': io_empty_util(), 'code_path': job['root_path'], 'depth': 0, 'code_ok': None}
