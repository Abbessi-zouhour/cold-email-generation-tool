from services.supabase_client import supabase


# =========================
# COMPANIES
# =========================

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


# =========================
# CONTACTS
# =========================

def get_crm_contacts(company_id=None):
    query = (
        supabase.table("crm_contacts")
        .select("*")
        .order("created_at", desc=True)
    )

    if company_id:
        query = query.eq("company_id", int(company_id))

    response = query.execute()
    return response.data if response.data else []
def crm_contact_exists(
    email,
    phone=None,
    exclude_contact_id=None
):
    query = (
        supabase.table("crm_contacts")
        .select("id,email,phone")
    )

    if phone:
        response = (
            query.or_(
                f"email.eq.{email},phone.eq.{phone}"
            )
            .execute()
        )
    else:
        response = (
            query.eq("email", email)
            .execute()
        )

    if not response.data:
        return False

    if exclude_contact_id is not None:
        return any(
            int(c["id"]) != int(exclude_contact_id)
            for c in response.data
        )

    return True

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


def update_crm_contact(contact_id, company_id, full_name, job_title, email, phone, linkedin):
    response = (
        supabase.table("crm_contacts")
        .update({
            "company_id": int(company_id),
            "full_name": full_name,
            "job_title": job_title,
            "email": email,
            "phone": phone,
            "linkedin": linkedin
        })
        .eq("id", int(contact_id))
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


# =========================
# FOLLOW-UPS
# =========================

def get_crm_followups(company_id=None):
    query = (
        supabase.table("crm_followups")
        .select("*")
        .order("followup_date", desc=False)
    )

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
def crm_company_exists(company_name, exclude_company_id=None):
    company_name = company_name.strip().lower()

    response = (
        supabase.table("crm_companies")
        .select("id, company_name")
        .ilike("company_name", company_name)
        .execute()
    )

    if not response.data:
        return False

    if exclude_company_id is not None:
        return any(int(c["id"]) != int(exclude_company_id) for c in response.data)

    return True

def crm_contact_exists(email, phone=None, exclude_contact_id=None):
    email = str(email).strip().lower()
    phone = str(phone).strip() if phone else ""

    if not email and not phone:
        return False

    query = supabase.table("crm_contacts").select("id,email,phone")

    if email and phone:
        response = query.or_(f"email.eq.{email},phone.eq.{phone}").execute()
    elif email:
        response = query.eq("email", email).execute()
    else:
        response = query.eq("phone", phone).execute()

    if not response.data:
        return False

    if exclude_contact_id is not None:
        return any(
            int(c["id"]) != int(exclude_contact_id)
            for c in response.data
        )

    return True