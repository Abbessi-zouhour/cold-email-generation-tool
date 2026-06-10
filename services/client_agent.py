from models.llm import get_llm


def generate_client_delay_message(
    client_name,
    service_type,
    delay_reason,
    original_deadline,
    new_delivery_date,
    tone="Professional"
):
    llm = get_llm()

    prompt = f"""
    Write a professional client update message for a recruitment/career services agency.

    Client name: {client_name}
    Service type: {service_type}
    Original deadline: {original_deadline}
    New delivery date: {new_delivery_date}
    Delay reason: {delay_reason}
    Tone: {tone}

    Requirements:
    - Include a clear subject line
    - Apologize politely
    - Explain the delay without sounding careless
    - Reassure the client that quality is the priority
    - Mention the new delivery date
    - Keep it human, respectful, and professional
    - Do not overpromise
    """

    response = llm.invoke(prompt)
    return response.content


def generate_client_progress_update(
    client_name,
    service_type,
    current_status,
    next_step,
    tone="Professional"
):
    llm = get_llm()

    prompt = f"""
    Write a professional progress update message for a client.

    Client name: {client_name}
    Service type: {service_type}
    Current status: {current_status}
    Next step: {next_step}
    Tone: {tone}

    Requirements:
    - Include a subject line
    - Sound human and professional
    - Clearly explain the current progress
    - Mention the next step
    - Keep the message concise
    """

    response = llm.invoke(prompt)
    return response.content