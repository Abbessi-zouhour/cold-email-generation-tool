import streamlit as st
from services.email_generator import generate_email

st.set_page_config(
    page_title="AI Cold Email Generator",
    page_icon="📧"
)

st.title("📧 AI Cold Email Generator")

job_role = st.text_input("Job Role")
company = st.text_input("Company")

if st.button("Generate Email"):
    if job_role and company:
        email = generate_email(job_role, company)

        st.subheader("Generated Email")
        st.write(email)
    else:
        st.warning("Please fill in all fields.")