from models.llm import get_llm

def generate_cover_letter(resume_text, job_description):
    llm = get_llm()

    prompt = f"""
    Write a professional, tailored cover letter based on the resume and job description.

    Resume:
    {resume_text}

    Job description:
    {job_description}

    Requirements:
    - Professional tone
    - Tailor the letter to the job description
    - Highlight relevant skills and experience from the resume
    - Do not invent experience
    - Keep it concise
    - Include a subject line
    """

    response = llm.invoke(prompt)
    return response.content