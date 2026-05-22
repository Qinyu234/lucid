from .generate_function_name import generate_function_name


def ipo_to_nodes(ipo):

    children = []

    for x in ipo.get("input", []) + \
             ipo.get("process", []) + \
             ipo.get("output", []):

        if not x:
            continue

        node = {

            "semantic": str(x),

            "function_name": None,

            "children": [],

            "status": "growing",

            "code_path": None

        }

        name = generate_function_name(node)

        # =========================
        # hard safety check
        # =========================

        if (
            not isinstance(name, str)
            or name.strip() == ""
        ):
            name = "node_" + str(abs(hash(x)))[:8]

        node["function_name"] = name

        children.append(node)

    return children