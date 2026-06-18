import pandas as pd
from services.supabase_client import supabase


def to_dataframe(response):
    data = response.data if response.data else []
    return pd.DataFrame(data)


# =========================
# CANDIDATES
# =========================

def get_candidates_supabase():
    response = (
        supabase.table("candidates")
        .select("*")
        .execute()
    )
    return to_dataframe(response)


def get_candidate_by_id_supabase(candidate_id):
    response = (
        supabase.table("candidates")
        .select("*")
        .eq("id", int(candidate_id))
        .execute()
    )
    return to_dataframe(response)


def add_candidate_supabase(
    name,
    email,
    phone,
    country,
    experience_years,
    languages,
    skills,
    status,
    pipeline_stage
):
    response = (
        supabase.table("candidates")
        .insert({
            "name": name,
            "email": email,
            "phone": phone,
            "country": country,
            "experience_years": int(experience_years),
            "languages": languages,
            "skills": skills,
            "status": status,
            "pipeline_stage": pipeline_stage
        })
        .execute()
    )

    return response.data


def update_candidate_supabase(
    candidate_id,
    name,
    email,
    phone,
    country,
    experience_years,
    languages,
    skills,
    status,
    pipeline_stage
):
    response = (
        supabase.table("candidates")
        .update({
            "name": name,
            "email": email,
            "phone": phone,
            "country": country,
            "experience_years": int(experience_years),
            "languages": languages,
            "skills": skills,
            "status": status,
            "pipeline_stage": pipeline_stage
        })
        .eq("id", int(candidate_id))
        .execute()
    )

    return response.data


def delete_candidate_supabase(candidate_id):
    response = (
        supabase.table("candidates")
        .delete()
        .eq("id", int(candidate_id))
        .execute()
    )

    return response.data


# =========================
# PIPELINE
# =========================

def update_candidate_stage_supabase(candidate_id, new_stage):
    response = (
        supabase.table("candidates")
        .update({
            "pipeline_stage": new_stage
        })
        .eq("id", int(candidate_id))
        .execute()
    )

    return response.data


# =========================
# TIMELINE
# =========================

def get_candidate_timeline_supabase(candidate_id):
    response = (
        supabase.table("candidate_timeline")
        .select("*")
        .eq("candidate_id", int(candidate_id))
        .order("event_date", desc=True)
        .execute()
    )

    return to_dataframe(response)


def add_timeline_event_supabase(
    candidate_id,
    event_date,
    event_type,
    notes
):
    response = (
        supabase.table("candidate_timeline")
        .insert({
            "candidate_id": int(candidate_id),
            "event_date": str(event_date),
            "event_type": event_type,
            "notes": notes
        })
        .execute()
    )

    return response.data


def delete_timeline_event_supabase(event_id):
    response = (
        supabase.table("candidate_timeline")
        .delete()
        .eq("id", int(event_id))
        .execute()
    )

    return response.data


# =========================
# JOBS
# =========================

def get_jobs_supabase():
    response = (
        supabase.table("jobs")
        .select("*")
        .execute()
    )

    return to_dataframe(response)


# =========================
# CLIENTS
# =========================

def get_clients_supabase():
    response = (
        supabase.table("clients")
        .select("*")
        .execute()
    )

    return to_dataframe(response)


# =========================
# INTERVIEWS
# =========================

def get_interviews_supabase():
    response = (
        supabase.table("interviews")
        .select("*")
        .execute()
    )

    return to_dataframe(response)
def add_interview_supabase(
    candidate_id,
    candidate_name,
    candidate_email,
    job_title,
    company,
    interview_date,
    interview_time,
    interview_type,
    notes,
    status="Scheduled"
):
    response = (
        supabase.table("interviews")
        .insert({
            "candidate_id": int(candidate_id),
            "candidate_name": candidate_name,
            "candidate_email": candidate_email,
            "job_title": job_title,
            "company": company,
            "interview_date": str(interview_date),
            "interview_time": str(interview_time),
            "interview_type": interview_type,
            "notes": notes,
            "status": status
        })
        .execute()
    )
    return response.data

def delete_interview_supabase(interview_id):
    response = (
        supabase.table("interviews")
        .delete()
        .eq("id", int(interview_id))
        .execute()
    )
    return response.data
def add_client_supabase(name, service, deadline, status):
    response = (
        supabase.table("clients")
        .insert({
            "name": name,
            "service": service,
            "deadline": str(deadline),
            "status": status
        })
        .execute()
    )
    return response.data


def update_client_supabase(client_id, name, service, deadline, status):
    response = (
        supabase.table("clients")
        .update({
            "name": name,
            "service": service,
            "deadline": str(deadline),
            "status": status
        })
        .eq("id", int(client_id))
        .execute()
    )
    return response.data


def delete_client_supabase(client_id):
    response = (
        supabase.table("clients")
        .delete()
        .eq("id", int(client_id))
        .execute()
    )
    return response.data