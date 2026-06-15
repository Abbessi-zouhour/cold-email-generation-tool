import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


def fetch_remotive_jobs(search="developer"):
    try:
        url = "https://remotive.com/api/remote-jobs"

        response = requests.get(
            url,
            params={"search": search},
            timeout=15
        )

        response.raise_for_status()

        jobs = response.json().get("jobs", [])

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

    except Exception as e:
        print("Remotive error:", e)
        return pd.DataFrame()


def fetch_adzuna_jobs(search="developer", country="gb"):
    try:
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

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            print("Adzuna error:", response.text)
            return pd.DataFrame()

        results = response.json().get("results", [])

        rows = []

        for i, job in enumerate(results, start=1):

            salary_min = job.get("salary_min")
            salary_max = job.get("salary_max")

            if salary_min and salary_max:
                salary_range = f"{salary_min}-{salary_max}"
            else:
                salary_range = "Not specified"

            rows.append({
                "id": i,
                "company": job.get("company", {}).get(
                    "display_name",
                    "Not specified"
                ),
                "country": job.get("location", {}).get(
                    "display_name",
                    country.upper()
                ),
                "job_title": job.get("title", ""),
                "required_skills": search,
                "experience_required": 0,
                "language_required": "Not specified",
                "salary_range": salary_range,
                "status": "Open",
                "job_link": job.get("redirect_url", "")
            })

        return pd.DataFrame(rows)

    except Exception as e:
        print("Adzuna error:", e)
        return pd.DataFrame()


def fetch_jsearch_jobs(search="developer", country="us"):
    try:

        if not RAPIDAPI_KEY:
            return pd.DataFrame()

        url = "https://jsearch.p.rapidapi.com/search"

        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

        params = {
            "query": f"{search} in {country}",
            "page": "1",
            "num_pages": "1"
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=20
        )

        if response.status_code != 200:
            print("JSearch error:", response.text)
            return pd.DataFrame()

        jobs = response.json().get("data", [])

        rows = []

        for i, job in enumerate(jobs, start=1):

            salary_min = job.get("job_min_salary")
            salary_max = job.get("job_max_salary")

            if salary_min and salary_max:
                salary_range = f"{salary_min}-{salary_max}"
            else:
                salary_range = "Not specified"

            rows.append({
                "id": i,
                "company": job.get("employer_name", ""),
                "country": job.get("job_country", ""),
                "job_title": job.get("job_title", ""),
                "required_skills": search,
                "experience_required": 0,
                "language_required": "Not specified",
                "salary_range": salary_range,
                "status": "Open",
                "job_link": job.get("job_apply_link", "")
            })

        return pd.DataFrame(rows)

    except Exception as e:
        print("JSearch error:", e)
        return pd.DataFrame()


def fetch_online_jobs(search="developer", country="gb"):

    all_jobs = []

    adzuna_jobs = fetch_adzuna_jobs(search, country)

    if not adzuna_jobs.empty:
        all_jobs.append(adzuna_jobs)

    jsearch_jobs = fetch_jsearch_jobs(search, country)

    if not jsearch_jobs.empty:
        all_jobs.append(jsearch_jobs)

    remotive_jobs = fetch_remotive_jobs(search)

    if not remotive_jobs.empty:
        all_jobs.append(remotive_jobs)

    if not all_jobs:
        return pd.DataFrame()

    jobs = pd.concat(all_jobs, ignore_index=True)

    jobs = jobs.drop_duplicates(
        subset=["company", "job_title"],
        keep="first"
    )

    jobs["id"] = range(1, len(jobs) + 1)

    return jobs