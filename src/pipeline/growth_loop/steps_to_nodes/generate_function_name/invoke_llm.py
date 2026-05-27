def invoke_llm(scenario, prompt, job_id=None):
    from src.shared.lib.llm_util import llm_util

    return llm_util(scenario, prompt, job_id=job_id)
