import pandas as pd

def calculate_match_score(candidate_skills, required_skills):
    candidate_skills = set(s.strip().lower() for s in candidate_skills.split(","))
    required_skills = set(s.strip().lower() for s in required_skills.split(","))

    matched_skills = candidate_skills.intersection(required_skills)

    if len(required_skills) == 0:
        score = 0
    else:
        score = int((len(matched_skills) / len(required_skills)) * 100)

    return score, list(matched_skills)


def match_candidates(job_id, candidates, jobs):
    job = jobs[jobs["id"] == job_id].iloc[0]
    results = []

    for _, candidate in candidates.iterrows():
        score, matched_skills = calculate_match_score(
            candidate["skills"],
            job["required_skills"]
        )

        if candidate["experience_years"] >= job["experience_required"]:
            score += 10

        score = min(score, 100)

        results.append({
            "candidate_name": candidate["name"],
            "email": candidate["email"],
            "country": candidate["country"],
            "experience_years": candidate["experience_years"],
            "skills": candidate["skills"],
            "matched_skills": ", ".join(matched_skills),
            "match_score": score,
            "status": candidate["status"]
        })

    return job, pd.DataFrame(results).sort_values("match_score", ascending=False)