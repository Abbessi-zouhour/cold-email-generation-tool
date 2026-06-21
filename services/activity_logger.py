from services.supabase_client import supabase


def log_activity(username, role, action, entity_type="", entity_id="", details=""):
    try:
        supabase.table("activity_logs").insert({
            "username": username,
            "role": role,
            "action": action,
            "entity_type": entity_type,
            "entity_id": str(entity_id),
            "details": details
        }).execute()
    except Exception:
        pass


def get_activity_logs():
    response = (
        supabase.table("activity_logs")
        .select("*")
        .order("created_at", desc=True)
        .limit(200)
        .execute()
    )
    return response.data if response.data else []