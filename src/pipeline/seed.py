from src.schema.io import empty_io


def seed(job):

    return {
        "function_name": job["id"],
        "semantic": job["goal"],
        "children": [],
        "topology": None,
        "status": "growing",
        "tag": None,
        "case": None,
        "io": empty_io(),
        "code_path": job["root_path"],
    }
