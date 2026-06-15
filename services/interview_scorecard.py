from models.llm import get_llm


def evaluate_candidate(job_title, questions, answers):
    llm = get_llm()

    prompt = f"""
    You are a senior recruiter.

    Job Title:
    {job_title}

    Interview Questions:
    {questions}

    Candidate Answers:
    {answers}

    Evaluate:

    1. Technical Score /100
    2. Communication Score /100
    3. Problem Solving Score /100
    4. Overall Score /100
    5. Hiring Recommendation

    Use one of:

    - Strong Hire
    - Hire
    - Maybe
    - Reject

    Give detailed reasoning.
    """

    response = llm.invoke(prompt)

    return response.content