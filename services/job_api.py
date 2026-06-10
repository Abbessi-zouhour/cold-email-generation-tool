import requests
import pandas as pd

def fetch_remotive_jobs(search="developer"):
    url = "https://remotive.com/api/remote-jobs"
    params = {"search": search}

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    jobs = data.get("jobs", [])

    rows = []

    for i, job in enumerate(jobs, start=1):
        rows.append({
            "id": i,
            "company": job.get("company_name", ""),
            "country": "Remote",
            "job_title": job.get("title", ""),
            "required_skills": search,
            "experience_required": 2,
            "language_required": "English",
            "salary_range": job.get("salary", "Not specified"),
            "status": "Open"
        })

    return pd.DataFrame(rows)