from services.supabase_client import supabase
from services.candidate_matcher import match_candidates


def generate_candidate_ranking(job_id, candidates, jobs, created_by):
    job, matches = match_candidates(job_id, candidates, jobs)

    saved_rankings = []

    for _, row in matches.head(10).iterrows():
        score = float(row.get("match_score", 0))

        strengths = f"Matched skills: {row.get('matched_skills', '')}"
        weaknesses = "Review missing job-specific skills manually."

        if score >= 80:
            recommendation = "Strong candidate. Recommended for interview."
        elif score >= 60:
            recommendation = "Good candidate. Review profile before shortlisting."
        elif score >= 40:
            recommendation = "Moderate match. Consider if talent pool is limited."
        else:
            recommendation = "Low match. Not recommended for this role."

        response = (
            supabase.table("candidate_rankings")
            .insert({
                "job_id": int(job_id),
                "candidate_id": int(row.get("id", row.get("candidate_id", 0))),
                "candidate_name": row.get("candidate_name", ""),
                "job_title": job.get("job_title", ""),
                "company": job.get("company", ""),
                "ranking_score": score,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "recommendation": recommendation,
                "created_by": created_by
            })
            .execute()
        )

        saved_rankings.extend(response.data if response.data else [])

    return job, matches.head(10), saved_rankings


def get_candidate_rankings(job_id=None):
    query = (
        supabase.table("candidate_rankings")
        .select("*")
        .order("ranking_score", desc=True)
    )

    if job_id:
        query = query.eq("job_id", int(job_id))

    response = query.execute()
    return response.data if response.data else []


def delete_candidate_ranking(ranking_id):
    response = (
        supabase.table("candidate_rankings")
        .delete()
        .eq("id", int(ranking_id))
        .execute()
    )
    return response.data