from .generate_function_name import generate_function_name


def ipo_to_nodes(ipo):

    children = []

    for x in ipo["input"] + ipo["process"] + ipo["output"]:

        node = {

            "semantic": x,

            # ⭐关键：这里必须生成符号
            "function_name": generate_function_name({
                "semantic": x
            }),

            "children": [],

            # ✔ 统一状态，不要 todo/growing 混用
            "status": "growing",

            "code_path": None

        }

        children.append(node)

    return children