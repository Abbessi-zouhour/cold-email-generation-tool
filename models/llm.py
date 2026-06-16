from dotenv import load_dotenv
import os
import streamlit as st
from langchain_groq import ChatGroq

load_dotenv()

def get_llm():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        api_key = st.secrets["GROQ_API_KEY"]

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.7
    )