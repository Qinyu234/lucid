def resolve_code_paths(root: dict):
    from src.shared.io_tree.child_code_path_util import child_code_path_util
    '\n    Composite node -> code_path is package directory under <job>/src/<pkg>/...\n    Leaf node -> code_path is module stem; file is f"{code_path}.py".\n    '

    def repair_leaf(node: dict) -> str:
        fn = node.get("function_name") or "unnamed"
        raw = str(node.get("code_path") or "").strip().replace("\\", "/").rstrip("/")
        base = raw.split("/")[-1] if raw else ""
        if base != fn:
            parent = "/".join(raw.split("/")[:-1]) if raw else ""
            node["code_path"] = child_code_path_util(parent, fn) if parent else fn
        return node.get("code_path") or fn

    def walk(node: dict, base_path: str):
        children = node.get('children') or []
        if children:
            node['code_path'] = base_path.rstrip('/\\')
            for child in children:
                cfn = child.get('function_name') or 'unnamed'
                walk(child, child_code_path_util(node['code_path'], cfn))
        else:
            node['code_path'] = base_path.rstrip('/\\')
    project_root = (root.get('code_path') or '').rstrip('/\\')
    fn = root.get('function_name') or 'root'
    pr = project_root.rstrip("/").rstrip("\\")
    root_base = (pr + "/src/" + fn).replace("\\", "/")
    walk(root, root_base)
    stack = [root]
    while stack:
        node = stack.pop()
        if not node.get('children'):
            repair_leaf(node)
        for child in node.get('children', []):
            stack.append(child)
