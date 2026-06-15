from models.llm import get_llm


def generate_interview_invitation_email(
    candidate_name,
    candidate_email,
    job_title,
    company,
    interview_date,
    interview_time,
    interview_type,
    notes=""
):
    llm = get_llm()

    prompt = f"""
You are a professional recruitment assistant.

Write a clear and professional interview invitation email.

Candidate name: {candidate_name}
Candidate email: {candidate_email}
Job title: {job_title}
Company: {company}
Interview date: {interview_date}
Interview time: {interview_time}
Interview type: {interview_type}
Additional notes: {notes}

The email must include:
- Professional greeting
- Interview details
- Confirmation request
- Polite closing

Do not invent contact details.
"""

    try:
        response = llm.invoke(prompt)

        if hasattr(response, "content"):
            return response.content

        return str(response)

    except Exception as e:
        return f"Error generating interview invitation email: {str(e)}"