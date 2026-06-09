import streamlit as st
from services.candidate_matcher import load_data, match_candidates
from services.email_generator import generate_email
from services.job_analyzer import analyze_job_offer
from services.cv_parser import parse_cv

st.set_page_config(
    page_title="AI Recruitment Agency Platform",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 AI Recruitment Agency Platform")

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Job Offers",
        "Candidates",
        "Candidate Matching",
        "Email Generator",
        "Job Analyzer",
        "CV Parser"
    ]
)

candidates, jobs = load_data()

if menu == "Dashboard":
    st.header("Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Candidates", len(candidates))
    col2.metric("Open Jobs", len(jobs[jobs["status"] == "Open"]))
    col3.metric("Available Candidates", len(candidates[candidates["status"] == "Available"]))

elif menu == "Job Offers":
    st.header("Job Offers")
    st.dataframe(jobs)

elif menu == "Candidates":
    st.header("Candidates")
    st.dataframe(candidates)

elif menu == "Candidate Matching":
    st.header("Candidate Matching")

    job_options = jobs["company"] + " - " + jobs["job_title"]
    selected_job = st.selectbox("Select Job Offer", job_options)

    job_index = job_options[job_options == selected_job].index[0]
    job_id = int(jobs.loc[job_index, "id"])

    job, matches = match_candidates(job_id)

    st.subheader(f"{job['company']} - {job['job_title']}")
    st.write(f"Country: {job['country']}")
    st.write(f"Required Skills: {job['required_skills']}")

    st.dataframe(matches)

elif menu == "Email Generator":
    st.header("Personalized Email Generator")

    job_options = jobs["company"] + " - " + jobs["job_title"]
    selected_job = st.selectbox("Select Job", job_options)

    job_index = job_options[job_options == selected_job].index[0]
    job_id = int(jobs.loc[job_index, "id"])

    job, matches = match_candidates(job_id)

    candidate_name = st.selectbox("Select Candidate", matches["candidate_name"])

    candidate = matches[matches["candidate_name"] == candidate_name].iloc[0]

    if st.button("Generate Email"):
        email = generate_email(
            candidate_name=candidate["candidate_name"],
            job_title=job["job_title"],
            company=job["company"],
            country=job["country"],
            matched_skills=candidate["matched_skills"]
        )

        st.subheader("Generated Email")
        st.write(email)

elif menu == "Job Analyzer":
    st.header("Job Offer Analyzer")

    job_description = st.text_area("Paste job offer here")

    if st.button("Analyze Job"):
        if job_description:
            result = analyze_job_offer(job_description)
            st.subheader("Analysis Result")
            st.write(result)
        else:
            st.warning("Please paste a job offer.")

elif menu == "CV Parser":
    st.header("CV Parser")

    cv_text = st.text_area("Paste CV text here")

    if st.button("Parse CV"):
        if cv_text:
            result = parse_cv(cv_text)
            st.subheader("Parsed CV")
            st.write(result)
        else:
            st.warning("Please paste CV text.")