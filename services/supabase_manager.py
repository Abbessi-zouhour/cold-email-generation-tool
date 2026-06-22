import pandas as pd
from services.supabase_client import supabase



def to_dataframe(response):
    data = response.data if response.data else []
    return pd.DataFrame(data)


# =========================
# CANDIDATES
# =========================

def get_candidates_supabase():
    try:
        response = (
            supabase.table("candidates")
            .select("*")
            .execute()
        )
        return to_dataframe(response)

    except Exception as e:
        print(f"Supabase error while loading candidates: {e}")
        return pd.DataFrame()

def get_candidate_by_id_supabase(candidate_id):
    response = (
        supabase.table("candidates")
        .select("*")
        .eq("id", int(candidate_id))
        .execute()
    )
    return to_dataframe(response)


def candidate_exists(email, phone=None, exclude_candidate_id=None):
    email = str(email).strip().lower()
    phone = str(phone).strip() if phone else ""

    if not email and not phone:
        return False

    query = supabase.table("candidates").select("id, email, phone")

    if email and phone:
        response = query.or_(f"email.eq.{email},phone.eq.{phone}").execute()
    elif email:
        response = query.eq("email", email).execute()
    else:
        response = query.eq("phone", phone).execute()

    if not response.data:
        return False

    if exclude_candidate_id is not None:
        return any(
            int(candidate["id"]) != int(exclude_candidate_id)
            for candidate in response.data
        )

    return True


def add_candidate_supabase(candidate_data):
    candidate_data["email"] = str(candidate_data.get("email", "")).strip().lower()
    candidate_data["phone"] = str(candidate_data.get("phone", "")).strip()

    return (
        supabase.table("candidates")
        .insert(candidate_data)
        .execute()
    )


def update_candidate_supabase(candidate_id, candidate_data):
    candidate_data["email"] = str(candidate_data.get("email", "")).strip().lower()
    candidate_data["phone"] = str(candidate_data.get("phone", "")).strip()

    return (
        supabase.table("candidates")
        .update(candidate_data)
        .eq("id", int(candidate_id))
        .execute()
    )


def delete_candidate_supabase(candidate_id):
    return (
        supabase.table("candidates")
        .delete()
        .eq("id", int(candidate_id))
        .execute()
    )


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


def add_timeline_event_supabase(candidate_id, event_date, event_type, notes):
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
    try:
        response = (
            supabase.table("jobs")
            .select("*")
            .execute()
        )
        return to_dataframe(response)

    except Exception as e:
        print(f"Supabase error while loading jobs: {e}")
        return pd.DataFrame()

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
def update_interview_supabase(
    interview_id,
    job_title,
    company,
    interview_date,
    interview_time,
    interview_type,
    notes,
    status
):
    response = (
        supabase.table("interviews")
        .update({
            "job_title": job_title,
            "company": company,
            "interview_date": str(interview_date),
            "interview_time": str(interview_time),
            "interview_type": interview_type,
            "notes": notes,
            "status": status
        })
        .eq("id", int(interview_id))
        .execute()
    )
    return response.data