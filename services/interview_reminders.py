from services.supabase_client import supabase


def create_interview_reminder(
    candidate_id,
    candidate_name,
    candidate_email,
    interview_date,
    interview_type
):
    response = (
        supabase.table("interview_reminders")
        .insert({
            "candidate_id": int(candidate_id),
            "candidate_name": candidate_name,
            "candidate_email": candidate_email,
            "interview_date": str(interview_date),
            "interview_type": interview_type,
            "reminder_sent": False
        })
        .execute()
    )
    return response.data


def get_interview_reminders():
    response = (
        supabase.table("interview_reminders")
        .select("*")
        .order("interview_date", desc=False)
        .execute()
    )
    return response.data if response.data else []


def get_pending_reminders():
    response = (
        supabase.table("interview_reminders")
        .select("*")
        .eq("reminder_sent", False)
        .order("interview_date", desc=False)
        .execute()
    )
    return response.data if response.data else []


def mark_reminder_sent(reminder_id):
    response = (
        supabase.table("interview_reminders")
        .update({"reminder_sent": True})
        .eq("id", int(reminder_id))
        .execute()
    )
    return response.data


def delete_interview_reminder(reminder_id):
    response = (
        supabase.table("interview_reminders")
        .delete()
        .eq("id", int(reminder_id))
        .execute()
    )
    return response.data
def delete_interview_reminder(reminder_id):
    response = (
        supabase.table("interview_reminders")
        .delete()
        .eq("id", int(reminder_id))
        .execute()
    )
    return response.data
def update_interview_reminder(
    reminder_id,
    interview_date,
    interview_type
):
    response = (
        supabase.table("interview_reminders")
        .update({
            "interview_date": str(interview_date),
            "interview_type": interview_type
        })
        .eq("id", int(reminder_id))
        .execute()
    )

    return response.data