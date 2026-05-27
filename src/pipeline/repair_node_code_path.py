def repair_node_code_path(node: dict, parent_path: str | None=None) -> str:
    from src.shared.io_tree.child_code_path_util import child_code_path_util

    def _basename(path: str) -> str:
        raw = (path or "").rstrip("/").rstrip("\\")
        if not raw:
            return ""
        raw = raw.replace("\\", "/")
        return raw.split("/")[-1]
    fn = node.get('function_name') or 'unnamed'
    if parent_path is not None:
        node['code_path'] = child_code_path_util(parent_path, fn)
        return node['code_path']
    path = (node.get('code_path') or '').strip()
    if not path or _basename(path) != fn:
        parent = "/".join((path.replace("\\", "/").rstrip("/").split("/")[:-1])) if path else ""
        node['code_path'] = child_code_path_util(parent, fn) if parent else fn
    return node['code_path']
