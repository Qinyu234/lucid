def recall_code(node, job_id=None):
    from src.pipeline.memory import recall_for_reuse

    return recall_for_reuse(node, job_id=job_id)
