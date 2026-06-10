def calculate_ats_score(cv_text, job_skills):
    cv_text = cv_text.lower()

    required_skills = [
        skill.strip().lower()
        for skill in job_skills.split(",")
        if skill.strip()
    ]

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill in cv_text:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if len(required_skills) == 0:
        score = 0
    else:
        score = int((len(matched_skills) / len(required_skills)) * 100)

    recommendations = [
        f"Add clear evidence of {skill} in your resume."
        for skill in missing_skills
    ]

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations
    }