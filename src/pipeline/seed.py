def seed(job):

    return {

        # =====================
        # system identity（原 id）
        # =====================
        "function_name": job["id"],

        # =====================
        # semantic layer
        # =====================
        "semantic": job["goal"],

        # =====================
        # structure
        # =====================
        "children": [],

        "status": "growing",

        # =====================
        # filesystem root
        # =====================
        "code_path": job["root_path"]

    }