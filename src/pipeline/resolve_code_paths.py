from src.pipeline.child_code_path import child_code_path
from src.pipeline.repair_node_code_path import repair_node_code_path


def resolve_code_paths(root: dict):
    """
    Composite node -> code_path is package directory.
    Leaf node -> code_path is module stem; file is f"{code_path}.py".
    """

    def walk(node: dict, base_path: str):
        children = node.get("children") or []

        if children:
            node["code_path"] = base_path.rstrip("/\\")
            for child in children:
                cfn = child.get("function_name") or "unnamed"
                walk(child, child_code_path(node["code_path"], cfn))
        else:
            node["code_path"] = base_path.rstrip("/\\")

    root_base = (root.get("code_path") or root.get("function_name") or "root").rstrip("/\\")
    walk(root, root_base)

    # leaf sanity: basename must equal function_name
    stack = [root]
    while stack:
        node = stack.pop()
        if not node.get("children"):
            repair_node_code_path(node)
        for child in node.get("children", []):
            stack.append(child)
