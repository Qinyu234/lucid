def assess_job(root, job=None) -> tuple:
    from pathlib import Path
    from src.pipeline.is_fully_grown import is_fully_grown

    def scaffold_issues(job_root: str) -> list:
        root_path = Path(job_root)
        out = []
        for name in ('src', 'io', 'requirement', 'tree', 'run.py'):
            if not (root_path / name).exists():
                out.append(f'scaffold: missing {name}')
        latest = root_path / 'tree' / 'latest.json'
        if not latest.is_file():
            out.append('scaffold: missing tree/latest.json')
        if (root_path / 'requirement').is_dir() and (not (root_path / 'requirement' / 'requirements.txt').exists()):
            out.append('scaffold: missing requirement/requirements.txt')
        if not (root_path / 'src' / 'shared' / '__init__.py').exists():
            out.append('scaffold: missing src/shared/__init__.py')
        return out

    def collect_issues(node, path: str='root') -> list:
        issues = []
        status = node.get('status')
        children = node.get('children', [])
        fn = node.get('function_name') or path
        here = f'{path}/{fn}' if path != 'root' else fn
        if status == 'growing':
            issues.append(f'{here}: still growing')
        if status == 'failed':
            issues.append(f"{here}: expand failed ({node.get('converge_reason')})")
        if node.get('code_ok') is False:
            issues.append(f'{here}: code generation failed')
        if status == 'done' and (not children) and (node.get('test_ok') is False):
            issues.append(f'{here}: test generation failed')
        for child in children:
            issues.extend(collect_issues(child, here))
        return issues
    issues = collect_issues(root)
    if job:
        issues.extend(scaffold_issues(job.get('root_path', '')))
    if issues:
        return ('incomplete', issues)
    if not is_fully_grown(root):
        return ('incomplete', ['tree growth did not converge'])
    return ('done', [])
