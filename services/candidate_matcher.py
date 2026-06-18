import re
import pandas as pd


def clean_skills(text):
    text = str(text).lower()
    parts = re.split(r"[,|/;-]+", text)
    return set(p.strip() for p in parts if p.strip())


def calculate_match_score(candidate, job):
    candidate_skills = clean_skills(candidate.get("skills", ""))
    required_skills = clean_skills(job.get("required_skills", ""))

    if not required_skills:
        skill_score = 0
        matched_skills = set()
    else:
        matched_skills = candidate_skills.intersection(required_skills)
        skill_score = (len(matched_skills) / len(required_skills)) * 70

    candidate_exp = int(candidate.get("experience_years", 0) or 0)
    required_exp = int(job.get("experience_required", 0) or 0)

    exp_score = 20 if candidate_exp >= required_exp else min(candidate_exp * 5, 20)

    country_score = 10 if str(candidate.get("country", "")).lower() in str(job.get("country", "")).lower() else 0

    total = skill_score + exp_score + country_score

    return round(min(total, 100), 2), list(matched_skills)


def match_candidates(job_id, candidates, jobs):
    job = jobs[jobs["id"].astype(float).astype(int) == int(job_id)].iloc[0]
    results = []

    for _, candidate in candidates.iterrows():
        score, matched_skills = calculate_match_score(candidate, job)

        results.append({
            "candidate_name": candidate.get("name", ""),
            "email": candidate.get("email", ""),
            "country": candidate.get("country", ""),
            "experience_years": candidate.get("experience_years", 0),
            "skills": candidate.get("skills", ""),
            "matched_skills": ", ".join(matched_skills),
            "match_score": score,
            "status": candidate.get("status", "")
        })

    return job, pd.DataFrame(results).sort_values("match_score", ascending=False)