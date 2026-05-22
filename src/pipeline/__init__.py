# =========================
# PIPELINE
# SEED → GROWTH → CODE → DONE
# =========================
from .seed import seed
from .growth_loop import growth_loop
from .code_tree import code_tree
from .is_fully_grown import is_fully_grown

def pipeline(job):

    # =========================
    # 1. SEED → root node
    # =========================
    root = seed(job)

    # =========================
    # 2. GROWTH → build tree
    # =========================
    growth_loop(root)

    # =========================
    # 3. CODE → compile leaves
    # =========================
    code_tree(root)

    # =========================
    # 4. FINAL CHECK
    # =========================
    status = "done" if is_fully_grown(root) else "incomplete"

    return {
        "job_id": job["id"],
        "status": status,
        "tree": root
    }