import pandas as pd


def _safe_float(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def recommend_candidates(job_row, candidates, top_n=5):
    job_skills = str(job_row.get("required_skills", "")).lower()
    job_title = str(job_row.get("job_title", "")).lower()
    job_country = str(job_row.get("country", "")).lower()
    job_language = str(job_row.get("language_required", "")).lower()
    job_experience = _safe_float(job_row.get("experience_required", 0))

    recommendations = []

    for _, candidate in candidates.iterrows():
        candidate_skills = str(candidate.get("skills", "")).lower()
        candidate_country = str(candidate.get("country", "")).lower()
        candidate_languages = str(candidate.get("languages", "")).lower()
        candidate_experience = _safe_float(candidate.get("experience_years", 0))

        skill_list = [
            skill.strip()
            for skill in candidate_skills.replace(";", ",").split(",")
            if skill.strip()
        ]

        matched_skills = [
            skill for skill in skill_list
            if skill in job_skills or skill in job_title
        ]

        skills_score = int((len(matched_skills) / len(skill_list)) * 100) if skill_list else 0

        if job_experience > 0:
            experience_score = 100 if candidate_experience >= job_experience else int((candidate_experience / job_experience) * 100)
        else:
            experience_score = 50

        country_score = 100 if candidate_country and candidate_country in job_country else 50
        language_score = 100 if candidate_languages and candidate_languages in job_language else 50

        match_score = int(
            skills_score * 0.40
            + experience_score * 0.30
            + country_score * 0.15
            + language_score * 0.15
        )

        if matched_skills or match_score >= 50:
            recommendations.append({
                "candidate_name": candidate.get("name", ""),
                "email": candidate.get("email", ""),
                "country": candidate.get("country", ""),
                "experience_years": candidate.get("experience_years", 0),
                "matched_skills": ", ".join(matched_skills) if matched_skills else "No direct skill match",
                "skills_score": skills_score,
                "experience_score": experience_score,
                "country_score": country_score,
                "language_score": language_score,
                "match_score": match_score
            })

    if not recommendations:
        return pd.DataFrame()

    return (
        pd.DataFrame(recommendations)
        .sort_values(by="match_score", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )