from models.llm import get_llm

def ask_assistant(question, candidates=None, jobs=None):
    llm = get_llm()

    context = f"""
    You are TalentBridge AI Assistant.
    Help users understand recruitment data, candidates, jobs, ATS scores,
    CV parsing, cover letters, and client communication.

    Candidates data preview:
    {candidates.head(10).to_string() if candidates is not None else "No candidates data"}

    Jobs data preview:
    {jobs.head(10).to_string() if jobs is not None else "No jobs data"}
    """

    prompt = f"""
    {context}

    User question:
    {question}

    Answer clearly and professionally.
    """

    response = llm.invoke(prompt)
    return response.content