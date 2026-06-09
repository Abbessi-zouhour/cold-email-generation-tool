import streamlit as st
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

st.title("📧 AI Cold Email Generator")

job_role = st.text_input("Job Role")
company = st.text_input("Company")

if st.button("Generate Email"):
    prompt = f"""
    Write a professional cold email for a candidate applying for a
    {job_role} position at {company}.

    The email should:
    - Be concise
    - Sound professional
    - Show enthusiasm
    - Ask for an opportunity to discuss further
    """

    response = llm.invoke(prompt)

    st.subheader("Generated Email")
    st.write(response.content)