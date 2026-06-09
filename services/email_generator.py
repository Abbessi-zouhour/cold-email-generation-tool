from models.llm import get_llm

def generate_email(candidate_name, job_title, company, country, matched_skills):
    llm = get_llm()

    prompt = f"""
    Write a professional recruitment agency email.

    Candidate: {candidate_name}
    Job title: {job_title}
    Company: {company}
    Country: {country}
    Matched skills: {matched_skills}

    The email should:
    - Be professional
    - Mention that our agency found an opportunity abroad
    - Mention the matched skills
    - Ask if the candidate is interested
    - Include a subject line
    """

    response = llm.invoke(prompt)
    return response.content