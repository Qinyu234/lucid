def build_tree(tasks: dict) -> dict:
    tree = {}

    for path, task in tasks.items():
        parts = path.split("/")  # 按路径分层
        node = tree

        # 逐级构建目录结构
        for part in parts[:-1]:
            node = node.setdefault(part, {})

        # 最后一层是文件
        file_name = parts[-1]
        node[file_name] = {
            "semantic": task.get("semantic"),
            "functions": task.get("functions", []),
            "imports": task.get("imports", [])
        }

    return tree