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
You are a professional Recruitment and Career Services Agency communication assistant.

Write a client delay update message.

Client name: {client_name}
Service type: {service_type}
Original deadline: {original_deadline}
New delivery date: {new_delivery_date}
Delay reason: {delay_reason}
Tone: {tone}

Requirements:
- Include a professional subject line
- Apologize politely
- Explain the delay professionally
- Reassure the client that quality and accuracy are priorities
- Mention the new delivery date
- Keep the message human, professional and concise
- Do not overpromise
- Do not invent phone numbers, emails, or names
- Do NOT use "[Your Name]"
- End the message exactly with:

Best regards,

Recruitment Team
"""

    try:
        response = llm.invoke(prompt)

        if hasattr(response, "content"):
            return response.content

        return str(response)

    except Exception as e:
        return f"Error generating delay message: {str(e)}"


def generate_client_progress_update(
    client_name,
    service_type,
    current_status,
    next_step,
    tone="Professional"
):
    llm = get_llm()

    prompt = f"""
You are a professional Recruitment and Career Services Agency communication assistant.

Write a client progress update message.

Client name: {client_name}
Service type: {service_type}
Current status: {current_status}
Next step: {next_step}
Tone: {tone}

Requirements:
- Include a professional subject line
- Clearly explain the current progress
- Mention the next step
- Sound professional and reassuring
- Keep the message concise
- Do not invent contact details
- Do NOT use "[Your Name]"
- End the message exactly with:

Best regards,

Recruitment Team
"""

    try:
        response = llm.invoke(prompt)

        if hasattr(response, "content"):
            return response.content

        return str(response)

    except Exception as e:
        return f"Error generating progress update: {str(e)}"