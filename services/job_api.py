import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")


def fetch_remotive_jobs(search="developer"):
    url = "https://remotive.com/api/remote-jobs"
    params = {"search": search}

    response = requests.get(url, params=params, timeout=15)
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
            "experience_required": 0,
            "language_required": "English",
            "salary_range": job.get("salary", "Not specified"),
            "status": "Open",
            "job_link": job.get("url", "")
        })

    return pd.DataFrame(rows)


def fetch_adzuna_jobs(search="developer", country="gb"):
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        return pd.DataFrame()

    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 50,
        "what": search,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params, timeout=15)

    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()
    results = data.get("results", [])

    rows = []

    for i, job in enumerate(results, start=1):
        company = job.get("company", {}).get("display_name", "Not specified")
        title = job.get("title", "")
        location = job.get("location", {}).get("display_name", country.upper())
        salary_min = job.get("salary_min", "")
        salary_max = job.get("salary_max", "")

        if salary_min and salary_max:
            salary_range = f"{salary_min}-{salary_max}"
        else:
            salary_range = "Not specified"

        rows.append({
            "id": i,
            "company": company,
            "country": location,
            "job_title": title,
            "required_skills": search,
            "experience_required": 0,
            "language_required": "Not specified",
            "salary_range": salary_range,
            "status": "Open",
            "job_link": job.get("redirect_url", "")
        })

    return pd.DataFrame(rows)


def fetch_online_jobs(search="developer", country="gb"):
    adzuna_jobs = fetch_adzuna_jobs(search, country)

    if not adzuna_jobs.empty:
        return adzuna_jobs

    return fetch_remotive_jobs(search)