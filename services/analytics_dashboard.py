def calculate_dashboard_metrics(candidates, jobs, clients, interviews):
    total_candidates = len(candidates)
    total_jobs = len(jobs)
    total_clients = len(clients)
    total_interviews = len(interviews)

    available_candidates = len(candidates[candidates["status"].astype(str) == "Available"]) if "status" in candidates.columns else 0
    hired_candidates = len(candidates[candidates["pipeline_stage"].astype(str) == "Hired"]) if "pipeline_stage" in candidates.columns else 0
    rejected_candidates = len(candidates[candidates["pipeline_stage"].astype(str) == "Rejected"]) if "pipeline_stage" in candidates.columns else 0
    open_jobs = len(jobs[jobs["status"].astype(str) == "Open"]) if "status" in jobs.columns else total_jobs

    hiring_rate = int((hired_candidates / total_candidates) * 100) if total_candidates > 0 else 0
    interview_rate = int((total_interviews / total_candidates) * 100) if total_candidates > 0 else 0

    return {
        "total_candidates": total_candidates,
        "total_jobs": total_jobs,
        "total_clients": total_clients,
        "total_interviews": total_interviews,
        "available_candidates": available_candidates,
        "hired_candidates": hired_candidates,
        "rejected_candidates": rejected_candidates,
        "open_jobs": open_jobs,
        "hiring_rate": hiring_rate,
        "interview_rate": interview_rate,
    }


def get_pipeline_counts(candidates):
    if "pipeline_stage" not in candidates.columns:
        return None

    return candidates["pipeline_stage"].astype(str).value_counts()


def get_status_counts(candidates):
    if "status" not in candidates.columns:
        return None

    return candidates["status"].astype(str).value_counts()


def get_country_counts(candidates):
    if "country" not in candidates.columns:
        return None

    return candidates["country"].astype(str).value_counts().head(10)


def get_jobs_by_country(jobs):
    if "country" not in jobs.columns:
        return None

    return jobs["country"].astype(str).value_counts().head(10)


def get_interviews_by_status(interviews):
    if interviews.empty or "status" not in interviews.columns:
        return None

    return interviews["status"].astype(str).value_counts()