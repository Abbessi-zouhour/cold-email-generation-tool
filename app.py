import streamlit as st
import pandas as pd

from services.candidate_matcher import load_data, match_candidates
from services.email_generator import generate_email
from services.job_analyzer import analyze_job_offer
from services.cv_parser import parse_cv


st.set_page_config(
    page_title="TalentBridge",
    page_icon="TB",
    layout="wide"
)


st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
    color: #111827;
}

.subtitle {
    font-size: 17px;
    color: #6b7280;
    margin-top: 6px;
}

.card {
    background: #ffffff;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    margin-bottom: 18px;
}

.kpi-card {
    background: #ffffff;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
}

.kpi-label {
    color: #6b7280;
    font-size: 14px;
}

.kpi-value {
    color: #111827;
    font-size: 34px;
    font-weight: 800;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 10px;
    color: #111827;
}

.logo-box {
    padding: 18px 10px 28px 10px;
}

.logo-main {
    font-size: 28px;
    font-weight: 800;
    color: #111827;
}

.logo-sub {
    font-size: 13px;
    color: #6b7280;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_data():
    return load_data()


candidates, jobs = get_data()


st.sidebar.markdown("""
<div class="logo-box">
    <div class="logo-main">TalentBridge</div>
    <div class="logo-sub">Recruitment Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
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


st.markdown("""
<h1 class="main-title">TalentBridge</h1>
<p class="subtitle">
A professional recruitment platform for matching talent with international job opportunities.
</p>
""", unsafe_allow_html=True)

st.divider()


if menu == "Dashboard":
    total_candidates = len(candidates)
    open_jobs = len(jobs[jobs["status"] == "Open"])
    available_candidates = len(candidates[candidates["status"] == "Available"])
    placed_candidates = len(candidates[candidates["status"] == "Placed"])

    st.markdown('<div class="section-title">Dashboard Overview</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Candidates</div>
            <div class="kpi-value">{total_candidates}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Open Positions</div>
            <div class="kpi-value">{open_jobs}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Available Talent</div>
            <div class="kpi-value">{available_candidates}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Placed Candidates</div>
            <div class="kpi-value">{placed_candidates}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([2, 1])

    with left:
        st.markdown("### Latest Job Opportunities")
        st.dataframe(
            jobs[["company", "country", "job_title", "experience_required", "salary_range", "status"]],
            use_container_width=True,
            hide_index=True
        )

    with right:
        st.markdown("### Talent Status")
        status_counts = candidates["status"].value_counts()

        for status, count in status_counts.items():
            st.markdown(f"""
            <div class="card">
                <div style="color:#6b7280;">{status}</div>
                <div style="font-size:30px; font-weight:800;">{count}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### Top Candidate Profiles")
    st.dataframe(
        candidates[["name", "country", "experience_years", "skills", "status"]].head(5),
        use_container_width=True,
        hide_index=True
    )


elif menu == "Job Offers":
    st.markdown('<div class="section-title">Job Offers</div>', unsafe_allow_html=True)

    country_filter = st.selectbox("Filter by country", ["All"] + sorted(jobs["country"].unique().tolist()))

    filtered_jobs = jobs.copy()
    if country_filter != "All":
        filtered_jobs = filtered_jobs[filtered_jobs["country"] == country_filter]

    st.dataframe(filtered_jobs, use_container_width=True, hide_index=True)


elif menu == "Candidates":
    st.markdown('<div class="section-title">Candidates</div>', unsafe_allow_html=True)

    status_filter = st.selectbox("Filter by status", ["All"] + sorted(candidates["status"].unique().tolist()))

    filtered_candidates = candidates.copy()
    if status_filter != "All":
        filtered_candidates = filtered_candidates[filtered_candidates["status"] == status_filter]

    st.dataframe(filtered_candidates, use_container_width=True, hide_index=True)


elif menu == "Candidate Matching":
    st.markdown('<div class="section-title">Candidate Matching</div>', unsafe_allow_html=True)

    job_options = jobs["company"] + " - " + jobs["job_title"]
    selected_job = st.selectbox("Select Job Offer", job_options)

    job_index = job_options[job_options == selected_job].index[0]
    job_id = int(jobs.loc[job_index, "id"])

    job, matches = match_candidates(job_id)

    st.markdown(f"""
    <div class="card">
        <h3>{job['company']} - {job['job_title']}</h3>
        <p><b>Country:</b> {job['country']}</p>
        <p><b>Required Skills:</b> {job['required_skills']}</p>
        <p><b>Experience Required:</b> {job['experience_required']} years</p>
        <p><b>Language Required:</b> {job['language_required']}</p>
        <p><b>Salary Range:</b> {job['salary_range']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Ranked Candidates")
    st.dataframe(matches, use_container_width=True, hide_index=True)

    chart_data = matches[["candidate_name", "match_score"]].set_index("candidate_name")
    st.bar_chart(chart_data)


elif menu == "Email Generator":
    st.markdown('<div class="section-title">Personalized Email Generator</div>', unsafe_allow_html=True)

    job_options = jobs["company"] + " - " + jobs["job_title"]
    selected_job = st.selectbox("Select Job", job_options)

    job_index = job_options[job_options == selected_job].index[0]
    job_id = int(jobs.loc[job_index, "id"])

    job, matches = match_candidates(job_id)

    if matches.empty:
        st.warning("No candidates found for this job.")
    else:
        candidate_name = st.selectbox("Select Candidate", matches["candidate_name"])
        candidate = matches[matches["candidate_name"] == candidate_name].iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="card">
                <h3>Candidate</h3>
                <p><b>Name:</b> {candidate['candidate_name']}</p>
                <p><b>Email:</b> {candidate['email']}</p>
                <p><b>Country:</b> {candidate['country']}</p>
                <p><b>Matched Skills:</b> {candidate['matched_skills']}</p>
                <p><b>Match Score:</b> {candidate['match_score']}%</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="card">
                <h3>Job Opportunity</h3>
                <p><b>Company:</b> {job['company']}</p>
                <p><b>Role:</b> {job['job_title']}</p>
                <p><b>Country:</b> {job['country']}</p>
                <p><b>Salary:</b> {job['salary_range']}</p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Generate Email", use_container_width=True):
            with st.spinner("Generating email..."):
                email = generate_email(
                    candidate_name=candidate["candidate_name"],
                    job_title=job["job_title"],
                    company=job["company"],
                    country=job["country"],
                    matched_skills=candidate["matched_skills"]
                )

            st.success("Email generated successfully.")
            st.text_area("Generated Email", email, height=300)


elif menu == "Job Analyzer":
    st.markdown('<div class="section-title">Job Offer Analyzer</div>', unsafe_allow_html=True)

    job_description = st.text_area(
        "Paste job offer here",
        height=260,
        placeholder="Paste the full job description here..."
    )

    if st.button("Analyze Job Offer", use_container_width=True):
        if job_description.strip():
            with st.spinner("Analyzing job offer..."):
                result = analyze_job_offer(job_description)

            st.success("Analysis completed.")
            st.markdown(result)
        else:
            st.warning("Please paste a job offer first.")


elif menu == "CV Parser":
    st.markdown('<div class="section-title">CV Parser</div>', unsafe_allow_html=True)

    cv_text = st.text_area(
        "Paste CV text here",
        height=260,
        placeholder="Paste candidate CV text here..."
    )

    if st.button("Parse CV", use_container_width=True):
        if cv_text.strip():
            with st.spinner("Parsing CV..."):
                result = parse_cv(cv_text)

            st.success("CV parsed successfully.")
            st.markdown(result)
        else:
            st.warning("Please paste CV text first.")