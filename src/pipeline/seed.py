# seed.py

def seed(job):
    return {
        "semantic": job["goal"],   # root semantic = goal
        "children": [],
        "status": "growing",
        "code_path": job["root_path"]
    }