def collect_growing_nodes(root):

    stack = [root]
    result = []

    while stack:

        node = stack.pop()

        if node.get("status") == "growing":
            result.append(node)

        for child in node.get("children", []):
            stack.append(child)

    return result