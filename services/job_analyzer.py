from models.llm import get_llm

def analyze_job_offer(job_description):
    llm = get_llm()

    prompt = f"""
    Analyze this job offer and extract:
    - Job title
    - Country
    - Required skills
    - Required experience
    - Required language
    - Salary if mentioned

    Job offer:
    {job_description}
    """

    response = llm.invoke(prompt)
    return response.content