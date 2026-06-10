import streamlit as st
import pandas as pd

from services.candidate_matcher import match_candidates
from services.email_generator import generate_email
from services.job_analyzer import analyze_job_offer
from services.cv_parser import parse_cv
from services.client_agent import generate_client_delay_message, generate_client_progress_update
from services.resume_reader import extract_text_from_pdf
from services.ats_score import calculate_ats_score
from services.cover_letter_generator import generate_cover_letter
from services.job_api import fetch_remotive_jobs
from services.assistant_agent import ask_assistant



st.set_page_config(
    page_title="TalentBridge",
    page_icon="TB",
    layout="wide"
)

st.markdown("""
<div class="hero-card">
    <div class="hero-title">TalentBridge</div>
    <div class="hero-subtitle">
        AI-Powered Recruitment Intelligence Platform
    </div>
</div>
""", unsafe_allow_html=True)


st.sidebar.markdown("### Upload Your Data")

uploaded_candidates = st.sidebar.file_uploader(
    "Upload candidates CSV",
    type=["csv"]
)
st.sidebar.markdown("### Search Online Jobs")

job_search_keyword = st.sidebar.text_input(
    "Search jobs online",
    value="python developer"
)

use_online_jobs = st.sidebar.button("Fetch Online Jobs")

uploaded_jobs = st.sidebar.file_uploader(
    "Upload jobs CSV",
    type=["csv"]
)

uploaded_clients = st.sidebar.file_uploader(
    "Upload clients CSV",
    type=["csv"]
)


def load_csv(uploaded_file, default_path):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return pd.read_csv(default_path)


candidates = load_csv(uploaded_candidates, "database/candidates.csv")

if use_online_jobs:
    jobs = fetch_remotive_jobs(job_search_keyword)
else:
    jobs = load_csv(uploaded_jobs, "database/jobs.csv")

clients = load_csv(uploaded_clients, "database/clients.csv")


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
        "Candidate Pipeline",
        "Email Generator",
        "Job Analyzer",
        "CV Parser",
        "ATS Score",
        "Cover Letter Generator",
        "Client Communication Agent",
        "AI Assistant"
        
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

elif menu == "ATS Score":
    st.markdown('<div class="section-title">ATS Score Calculator</div>', unsafe_allow_html=True)

    st.caption("Upload a resume PDF and compare it against a selected job offer.")

    job_options = jobs["company"] + " - " + jobs["job_title"]
    selected_job = st.selectbox("Select Target Job", job_options)

    job_index = job_options[job_options == selected_job].index[0]
    job = jobs.loc[job_index]

    st.markdown(f"""
    <div class="card">
        <h3>{job['company']} - {job['job_title']}</h3>
        <p><b>Country:</b> {job['country']}</p>
        <p><b>Required Skills:</b> {job['required_skills']}</p>
        <p><b>Experience Required:</b> {job['experience_required']} years</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )

    cv_text = ""

    if uploaded_file is not None:
        cv_text = extract_text_from_pdf(uploaded_file)
        st.success("Resume uploaded successfully.")

        with st.expander("Preview extracted resume text"):
            st.text_area("Extracted Resume Text", cv_text, height=220)

    if st.button("Calculate ATS Score", use_container_width=True):
        if cv_text.strip():
            result = calculate_ats_score(
                cv_text=cv_text,
                job_skills=job["required_skills"]
            )

            st.markdown("### ATS Result")

            st.metric("ATS Score", f"{result['score']}%")
            st.progress(result["score"] / 100)

            col1, col2 = st.columns(2)

            with col1:
                st.success("Matched Skills")
                if result["matched_skills"]:
                    for skill in result["matched_skills"]:
                        st.write(f"✅ {skill}")
                else:
                    st.write("No matched skills found.")

            with col2:
                st.warning("Missing Skills")
                if result["missing_skills"]:
                    for skill in result["missing_skills"]:
                        st.write(f"⚠️ {skill}")
                else:
                    st.write("No missing skills. Great match!")

            st.info("Improvement Suggestions")

            if result["recommendations"]:
                for recommendation in result["recommendations"]:
                    st.write(f"• {recommendation}")
            else:
                st.write("The resume already covers all required skills.")

        else:
            st.warning("Please upload a resume PDF first.")
elif menu == "Candidate Matching":
    st.markdown('<div class="section-title">Candidate Matching</div>', unsafe_allow_html=True)

    job_options = jobs["company"] + " - " + jobs["job_title"]
    selected_job = st.selectbox("Select Job Offer", job_options)

    job_index = job_options[job_options == selected_job].index[0]
    job_id = int(jobs.loc[job_index, "id"])

    job, matches = match_candidates(job_id, candidates, jobs) 

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

    job, matches = match_candidates(job_id, candidates, jobs)
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

    uploaded_file = st.file_uploader(
        "Upload CV as PDF",
        type=["pdf"]
    )

    final_cv_text = ""

    if uploaded_file is not None:
        final_cv_text = extract_text_from_pdf(uploaded_file)
        st.success("PDF uploaded and text extracted successfully.")

        with st.expander("Preview extracted CV text"):
            st.text_area("Extracted Text", final_cv_text, height=220)

    if st.button("Parse CV", use_container_width=True):
        if final_cv_text.strip():
            with st.spinner("Parsing CV..."):
                result = parse_cv(final_cv_text)

            st.success("CV parsed successfully.")
            st.markdown(result)
        else:
            st.warning("Please upload a PDF CV first.")
elif menu == "Client Communication Agent":
    st.markdown('<div class="section-title">Client Communication Agent</div>', unsafe_allow_html=True)

    st.caption("Generate professional client messages for delays, progress updates, and service communication.")

    tab1, tab2, tab3 = st.tabs([
        "Delay Message",
        "Progress Update",
        "Client Records"
    ])

    with tab1:
        st.subheader("Delay Message Generator")

        client_options = clients["name"] + " - " + clients["service"]
        selected_client = st.selectbox("Select Client", client_options)

        client_index = client_options[client_options == selected_client].index[0]
        client = clients.loc[client_index]

        col1, col2 = st.columns(2)

        with col1:
            client_name = st.text_input("Client Name", value=client["name"])
            service_type = st.text_input("Service Type", value=client["service"])
            original_deadline = st.text_input("Original Deadline", value=client["deadline"])

        with col2:
            delay_reason = st.selectbox(
                "Delay Reason",
                [
                    "Additional quality review",
                    "High workload",
                    "Missing client information",
                    "Personalized customization",
                    "Technical issue",
                    "Internal review delay"
                ]
            )

            new_delivery_date = st.date_input("New Delivery Date")

            tone = st.selectbox(
                "Tone",
                [
                    "Professional",
                    "Friendly",
                    "Apologetic",
                    "Formal",
                    "Reassuring"
                ]
            )

        if st.button("Generate Delay Message", use_container_width=True):
            with st.spinner("Generating message..."):
                message = generate_client_delay_message(
                    client_name=client_name,
                    service_type=service_type,
                    delay_reason=delay_reason,
                    original_deadline=original_deadline,
                    new_delivery_date=new_delivery_date,
                    tone=tone
                )

            st.success("Delay message generated successfully.")
            st.text_area("Generated Message", message, height=320)

    with tab2:
        st.subheader("Progress Update Generator")

        client_options_update = clients["name"] + " - " + clients["service"]
        selected_client_update = st.selectbox(
            "Select Client for Update",
            client_options_update,
            key="progress_client"
        )

        client_index_update = client_options_update[client_options_update == selected_client_update].index[0]
        client_update = clients.loc[client_index_update]

        col1, col2 = st.columns(2)

        with col1:
            progress_client_name = st.text_input(
                "Client Name",
                value=client_update["name"],
                key="progress_name"
            )

            progress_service_type = st.text_input(
                "Service Type",
                value=client_update["service"],
                key="progress_service"
            )

        with col2:
            current_status = st.selectbox(
                "Current Status",
                [
                    "Pending",
                    "In Progress",
                    "Under Review",
                    "Delayed",
                    "Completed"
                ]
            )

            next_step = st.text_input(
                "Next Step",
                placeholder="Example: Final review before sending the resume"
            )

            progress_tone = st.selectbox(
                "Tone",
                [
                    "Professional",
                    "Friendly",
                    "Formal",
                    "Reassuring"
                ],
                key="progress_tone"
            )

        if st.button("Generate Progress Update", use_container_width=True):
            if next_step.strip():
                with st.spinner("Generating progress update..."):
                    message = generate_client_progress_update(
                        client_name=progress_client_name,
                        service_type=progress_service_type,
                        current_status=current_status,
                        next_step=next_step,
                        tone=progress_tone
                    )

                st.success("Progress update generated successfully.")
                st.text_area("Generated Update", message, height=320)
            else:
                st.warning("Please enter the next step.")

    with tab3:
        st.subheader("Client Records")

        status_filter = st.selectbox(
            "Filter by Status",
            ["All"] + sorted(clients["status"].unique().tolist())
        )

        filtered_clients = clients.copy()

        if status_filter != "All":
            filtered_clients = filtered_clients[filtered_clients["status"] == status_filter]

        st.dataframe(
            filtered_clients,
            use_container_width=True,
            hide_index=True
        )
elif menu == "Candidate Pipeline":
    st.markdown('<div class="section-title">Candidate Pipeline</div>', unsafe_allow_html=True)

    st.caption("Track candidates across the recruitment process.")

    stages = [
        "Applied",
        "Screening",
        "Interview Scheduled",
        "Client Review",
        "Offer Sent",
        "Hired",
        "Rejected"
    ]

    cols = st.columns(len(stages))

    for col, stage in zip(cols, stages):
        with col:
            st.markdown(f"#### {stage}")

            stage_candidates = candidates[candidates["pipeline_stage"] == stage]

            if stage_candidates.empty:
                st.caption("No candidates")
            else:
                for _, candidate in stage_candidates.iterrows():
                    st.markdown(f"""
                    <div class="card">
                        <b>{candidate['name']}</b><br>
                        <span style="color:#6b7280;">{candidate['country']}</span><br>
                        <span>{candidate['experience_years']} years experience</span><br>
                        <small>{candidate['skills']}</small>
                    </div>
                    """, unsafe_allow_html=True)

elif menu == "Cover Letter Generator":
    st.markdown('<div class="section-title">Cover Letter Generator</div>', unsafe_allow_html=True)

    st.caption("Upload a resume PDF and paste the job description to generate a tailored cover letter.")

    uploaded_resume = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )

    job_description = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder="Paste the full job description here..."
    )

    resume_text = ""

    if uploaded_resume is not None:
        resume_text = extract_text_from_pdf(uploaded_resume)
        st.success("Resume uploaded successfully.")

        with st.expander("Preview extracted resume text"):
            st.text_area("Resume Text", resume_text, height=220)

    if st.button("Generate Cover Letter", use_container_width=True):
        if resume_text.strip() and job_description.strip():
            with st.spinner("Generating cover letter..."):
                cover_letter = generate_cover_letter(
                    resume_text=resume_text,
                    job_description=job_description
                )

            st.success("Cover letter generated successfully.")
            st.text_area("Generated Cover Letter", cover_letter, height=400)
        else:
            st.warning("Please upload a resume PDF and paste a job description.")
elif menu == "AI Assistant":
    st.markdown('<div class="section-title">AI Assistant</div>', unsafe_allow_html=True)

    st.caption("Ask questions about candidates, jobs, resumes, ATS scores, or recruitment workflows.")

    user_question = st.chat_input("Ask TalentBridge AI...")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if user_question:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):
            st.write(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_assistant(user_question, candidates, jobs)
                st.write(answer)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })