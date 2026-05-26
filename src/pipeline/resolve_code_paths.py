def resolve_code_paths(root: dict):
    import os
    from src.pipeline.child_code_path import child_code_path
    from src.pipeline.repair_node_code_path import repair_node_code_path
    '\n    Composite node -> code_path is package directory under <job>/src/<pkg>/...\n    Leaf node -> code_path is module stem; file is f"{code_path}.py".\n    '

    def walk(node: dict, base_path: str):
        children = node.get('children') or []
        if children:
            node['code_path'] = base_path.rstrip('/\\')
            for child in children:
                cfn = child.get('function_name') or 'unnamed'
                walk(child, child_code_path(node['code_path'], cfn))
        else:
            node['code_path'] = base_path.rstrip('/\\')
    project_root = (root.get('code_path') or '').rstrip('/\\')
    fn = root.get('function_name') or 'root'
    root_base = os.path.join(project_root, 'src', fn).replace('\\', '/')
    walk(root, root_base)
    stack = [root]
    while stack:
        node = stack.pop()
        if not node.get('children'):
            repair_node_code_path(node)
        for child in node.get('children', []):
            stack.append(child)
