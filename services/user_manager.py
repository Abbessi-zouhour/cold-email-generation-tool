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