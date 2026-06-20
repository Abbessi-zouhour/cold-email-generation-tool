import bcrypt
from services.supabase_client import supabase


def get_user(username, password):
    response = (
        supabase.table("app_users")
        .select("*")
        .eq("username", username)
        .eq("is_active", True)
        .execute()
    )

    if not response.data:
        return None

    user = response.data[0]

    stored_hash = user.get("password", "")

    try:
        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_hash.encode("utf-8")
        ):
            return user
    except Exception:
        return None

    return None


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def update_password(username, new_password):
    hashed_password = hash_password(new_password)

    return (
        supabase.table("app_users")
        .update({"password": hashed_password})
        .eq("username", username)
        .execute()
    )
def get_all_users():
    response = (
        supabase.table("app_users")
        .select("id, username, role, is_active, created_at")
        .order("id", desc=False)
        .execute()
    )
    return response.data if response.data else []


def create_user(username, password, role="Recruiter", is_active=True):
    username = username.strip().lower()
    hashed_password = hash_password(password)

    return (
        supabase.table("app_users")
        .insert({
            "username": username,
            "password": hashed_password,
            "role": role,
            "is_active": is_active
        })
        .execute()
    )

def update_user(user_id, username, role, is_active):
    username = username.strip().lower()

    return (
        supabase.table("app_users")
        .update({
            "username": username,
            "role": role,
            "is_active": is_active
        })
        .eq("id", int(user_id))
        .execute()
    )


def delete_user(user_id):
    return (
        supabase.table("app_users")
        .delete()
        .eq("id", int(user_id))
        .execute()
    )
def username_exists(username, exclude_user_id=None):
    username = username.strip().lower()

    response = (
        supabase.table("app_users")
        .select("id, username")
        .ilike("username", username)
        .execute()
    )

    if not response.data:
        return False

    if exclude_user_id is not None:
        return any(int(u["id"]) != int(exclude_user_id) for u in response.data)

    return True