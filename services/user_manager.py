from services.supabase_client import supabase


def get_user(username, password):
    response = (
        supabase.table("app_users")
        .select("*")
        .eq("username", username)
        .eq("password", password)
        .eq("is_active", True)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


def update_password(username, new_password):
    return (
        supabase.table("app_users")
        .update({"password": new_password})
        .eq("username", username)
        .execute()
    )