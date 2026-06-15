from models.llm import get_llm


def generate_interview_questions(
    resume_text,
    job_title,
    skills,
    job_description=""
):
    llm = get_llm()

    prompt = f"""
You are a senior technical recruiter and interview evaluator.

Create a complete interview kit for the following candidate and job.

Candidate Resume:
{resume_text}

Job Title:
{job_title}

Required Skills:
{skills}

Job Description:
{job_description}

Return the answer in this exact structure:

# Technical Questions

For each question include:
- Question
- Expected Answer
- Evaluation Criteria
- Difficulty

Generate 5 technical questions.

# HR Questions

For each question include:
- Question
- Expected Answer
- Evaluation Criteria
- Difficulty

Generate 3 HR questions.

# Behavioral Questions

For each question include:
- Question
- Expected Answer
- Evaluation Criteria
- Difficulty

Generate 3 behavioral questions.

# Practical Case Study

Include:
- Task
- Expected Approach
- Evaluation Criteria
- Difficulty

# Final Recruiter Notes

Give a short recommendation on how the recruiter should assess this candidate.
"""

    try:
        response = llm.invoke(prompt)

        if hasattr(response, "content"):
            return response.content

        return str(response)

    except Exception as e:
        return f"Error generating interview kit: {str(e)}"