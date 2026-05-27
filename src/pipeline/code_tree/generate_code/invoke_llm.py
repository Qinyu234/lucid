def invoke_llm(scenario, prompt, job_id=None):
    from src.llm import llm

    return llm(scenario, prompt, job_id=job_id)
