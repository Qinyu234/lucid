def ipo_to_nodes(ipo):

    children = []

    for x in ipo["input"]:
        children.append({
            "semantic": x,
            "children": [],
            "status": "todo",
            "code_path": None
        })

    for x in ipo["process"]:
        children.append({
            "semantic": x,
            "children": [],
            "status": "todo",
            "code_path": None
        })

    for x in ipo["output"]:
        children.append({
            "semantic": x,
            "children": [],
            "status": "todo",
            "code_path": None
        })

    return children