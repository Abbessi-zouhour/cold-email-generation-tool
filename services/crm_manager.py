from services.supabase_client import supabase


# Companies
def get_crm_companies():
    response = (
        supabase.table("crm_companies")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data if response.data else []


def add_crm_company(company_name, industry, country, website, status, owner):
    response = (
        supabase.table("crm_companies")
        .insert({
            "company_name": company_name,
            "industry": industry,
            "country": country,
            "website": website,
            "status": status,
            "owner": owner
        })
        .execute()
    )
    return response.data


def update_crm_company(company_id, company_name, industry, country, website, status, owner):
    response = (
        supabase.table("crm_companies")
        .update({
            "company_name": company_name,
            "industry": industry,
            "country": country,
            "website": website,
            "status": status,
            "owner": owner
        })
        .eq("id", int(company_id))
        .execute()
    )
    return response.data


def delete_crm_company(company_id):
    response = (
        supabase.table("crm_companies")
        .delete()
        .eq("id", int(company_id))
        .execute()
    )
    return response.data


# Contacts
def get_crm_contacts(company_id=None):
    query = supabase.table("crm_contacts").select("*").order("created_at", desc=True)

    if company_id:
        query = query.eq("company_id", int(company_id))

    response = query.execute()
    return response.data if response.data else []


def add_crm_contact(company_id, full_name, job_title, email, phone, linkedin):
    response = (
        supabase.table("crm_contacts")
        .insert({
            "company_id": int(company_id),
            "full_name": full_name,
            "job_title": job_title,
            "email": email,
            "phone": phone,
            "linkedin": linkedin
        })
        .execute()
    )
    return response.data


def delete_crm_contact(contact_id):
    response = (
        supabase.table("crm_contacts")
        .delete()
        .eq("id", int(contact_id))
        .execute()
    )
    return response.data


# Follow-ups
def get_crm_followups(company_id=None):
    query = supabase.table("crm_followups").select("*").order("followup_date", desc=False)

    if company_id:
        query = query.eq("company_id", int(company_id))

    response = query.execute()
    return response.data if response.data else []


def add_crm_followup(company_id, contact_id, followup_type, notes, followup_date, status, created_by):
    response = (
        supabase.table("crm_followups")
        .insert({
            "company_id": int(company_id),
            "contact_id": int(contact_id) if contact_id else None,
            "followup_type": followup_type,
            "notes": notes,
            "followup_date": str(followup_date),
            "status": status,
            "created_by": created_by
        })
        .execute()
    )
    return response.data


def update_crm_followup_status(followup_id, status):
    response = (
        supabase.table("crm_followups")
        .update({"status": status})
        .eq("id", int(followup_id))
        .execute()
    )
    return response.data


def delete_crm_followup(followup_id):
    response = (
        supabase.table("crm_followups")
        .delete()
        .eq("id", int(followup_id))
        .execute()
    )
    return response.data