from services.supabase_client import supabase


def get_candidate_notes(candidate_id):
    response = (
        supabase.table("candidate_notes")
        .select("*")
        .eq("candidate_id", int(candidate_id))
        .order("created_at", desc=True)
        .execute()
    )

    return response.data if response.data else []


def add_candidate_note(candidate_id, note, created_by):
    response = (
        supabase.table("candidate_notes")
        .insert({
            "candidate_id": int(candidate_id),
            "note": note,
            "created_by": created_by
        })
        .execute()
    )

    return response.data


def delete_candidate_note(note_id):
    response = (
        supabase.table("candidate_notes")
        .delete()
        .eq("id", int(note_id))
        .execute()
    )

    return response.data