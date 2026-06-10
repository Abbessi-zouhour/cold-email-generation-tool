from models.llm import get_llm


def parse_cv(cv_text):
    llm = get_llm()

    prompt = f"""
    Extract candidate information from this CV:

    Return:
    - Name
    - Email
    - Phone
    - Country
    - Skills
    - Experience years
    - Languages

    CV:
    {cv_text}
    """

    response = llm.invoke(prompt)
    return response.content