import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image

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

from database_manager import get_candidates, get_jobs, get_clients

BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "assets" / "images" / "logo.png"

logo_icon = Image.open(LOGO_PATH) if LOGO_PATH.exists() else "TB"

st.set_page_config(
    page_title="TalentBridge",
    page_icon=logo_icon,
    layout="wide"
)


def load_css():
    css_path = BASE_DIR / "assets" / "main.css"
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

menu_options = [
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

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# Sidebar
if LOGO_PATH.exists():
    st.sidebar.image(str(LOGO_PATH), use_container_width=True)

st.sidebar.markdown(
    "<div class='sidebar-subtitle'>Recruitment Intelligence Platform</div>",
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "Navigation",
    menu_options,
    index=menu_options.index(st.session_state.page)
)
st.session_state.page = menu

st.sidebar.markdown("### Upload Your Data")

uploaded_candidates = st.sidebar.file_uploader("Upload candidates CSV", type=["csv"])
uploaded_jobs = st.sidebar.file_uploader("Upload jobs CSV", type=["csv"])
uploaded_clients = st.sidebar.file_uploader("Upload clients CSV", type=["csv"])

st.sidebar.markdown("### Search Online Jobs")
job_search_keyword = st.sidebar.text_input("Search jobs online", value="python developer")
use_online_jobs = st.sidebar.button("Fetch Online Jobs")

# SQLite loading
if uploaded_candidates is not None:
    candidates = pd.read_csv(uploaded_candidates)
else:
    candidates = get_candidates()

if use_online_jobs:
    jobs = fetch_remotive_jobs(job_search_keyword)
elif uploaded_jobs is not None:
    jobs = pd.read_csv(uploaded_jobs)
else:
    jobs = get_jobs()

if uploaded_clients is not None:
    clients = pd.read_csv(uploaded_clients)
else:
    clients = get_clients()

# Top navigation
st.markdown("<div class='top-spacer'></div>", unsafe_allow_html=True)

brand_col, nav_col = st.columns([1.5, 3])

with brand_col:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=220)
    else:
        st.markdown("<h3>TalentBridge</h3>", unsafe_allow_html=True)

with nav_col:
    nav1, nav2, nav3, nav4 = st.columns(4)

    with nav1:
        if st.button("Dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()

    with nav2:
        if st.button("Candidates", use_container_width=True):
            st.session_state.page = "Candidates"
            st.rerun()

    with nav3:
        if st.button("Pipeline", use_container_width=True):
            st.session_state.page = "Candidate Pipeline"
            st.rerun()

    with nav4:
        if st.button("AI Assistant", use_container_width=True):
            st.session_state.page = "AI Assistant"
            st.rerun()

menu = st.session_state.page
st.divider()

if menu == "Dashboard":
    total_candidates = len(candidates)
    open_jobs = len(jobs[jobs["status"] == "Open"])
    available_candidates = len(candidates[candidates["status"] == "Available"])
    placed_candidates = len(candidates[candidates["status"] == "Placed"])

    st.markdown(f"""
    <h1 class="hero-title">AI-powered <span>recruitment intelligence</span> platform</h1>
    <p class="hero-subtitle">
        Manage candidates, analyze resumes, calculate ATS scores, match jobs,
        and get AI-powered recruitment insights in one platform.
    </p>

    <div class="stats-grid">
        <div class="stat"><h2>{total_candidates}</h2><p>Total candidates</p></div>
        <div class="stat"><h2>{open_jobs}</h2><p>Open positions</p></div>
        <div class="stat"><h2>{available_candidates}</h2><p>Available talent</p></div>
        <div class="stat"><h2>{placed_candidates}</h2><p>Placed candidates</p></div>
    </div>

    <div class="section">
        <div class="section-eyebrow">FEATURES</div>
        <h2 class="section-title">Everything recruiters need</h2>
        <p class="section-subtitle">
            AI-powered recruitment workflows for candidates, jobs, resumes and client communication.
        </p>
    </div>
    """, unsafe_allow_html=True)

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
                <div style="font-size:30px; font-weight:600;">{count}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### Top Candidate Profiles")

    for _, candidate in candidates.head(5).iterrows():
        st.markdown(f"""
        <div class="card" style="margin-bottom:12px;">
            <h3>{candidate['name']}</h3>
            <p>{candidate['country']} • {candidate['experience_years']} years experience</p>
            <p><b>Skills:</b> {candidate['skills']}</p>
            <span class="tag tag-matched">{candidate['status']}</span>
        </div>
        """, unsafe_allow_html=True)

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

elif menu == "Candidate Pipeline":
    st.markdown("""
    <div class="section-eyebrow">PIPELINE</div>
    <h2 class="section-title">Candidate pipeline</h2>
    <p class="section-subtitle">Track candidates across the recruitment process.</p>
    """, unsafe_allow_html=True)

    stages = ["Applied", "Screening", "Interview Scheduled", "Client Review", "Offer Sent", "Hired", "Rejected"]
    pipeline_html = '<div class="kanban-board">'

    for stage in stages:
        stage_candidates = candidates[candidates["pipeline_stage"] == stage]
        pipeline_html += f"""
        <div class="kanban-column">
            <div class="kanban-header">
                <span>{stage}</span>
                <span class="count-badge">{len(stage_candidates)}</span>
            </div>
        """

        if stage_candidates.empty:
            pipeline_html += '<p class="candidate-meta">No candidates</p>'
        else:
            for _, candidate in stage_candidates.iterrows():
                skills = str(candidate["skills"])
                main_skill = skills.split(",")[0].strip()
                skill_class = "tag-python"
                if "react" in main_skill.lower():
                    skill_class = "tag-react"
                elif "devops" in main_skill.lower() or "docker" in main_skill.lower():
                    skill_class = "tag-devops"
                elif "data" in main_skill.lower() or "sql" in main_skill.lower():
                    skill_class = "tag-data"
                elif "ml" in main_skill.lower() or "machine" in main_skill.lower():
                    skill_class = "tag-ml"

                pipeline_html += f"""
                <div class="candidate-card">
                    <div class="candidate-name">{candidate['name']}</div>
                    <div class="candidate-meta">{candidate['experience_years']} years • {candidate['country']}</div>
                    <span class="tag {skill_class}">{main_skill}</span>
                </div>
                """

        pipeline_html += "</div>"
    pipeline_html += "</div>"
    st.markdown(pipeline_html, unsafe_allow_html=True)

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

    uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
    cv_text = ""
    if uploaded_file is not None:
        cv_text = extract_text_from_pdf(uploaded_file)
        st.success("Resume uploaded successfully.")
        with st.expander("Preview extracted resume text"):
            st.text_area("Extracted Resume Text", cv_text, height=220)

    if st.button("Calculate ATS Score", use_container_width=True):
        if cv_text.strip():
            result = calculate_ats_score(cv_text=cv_text, job_skills=job["required_skills"])
            st.metric("ATS Score", f"{result['score']}%")
            st.progress(result["score"] / 100)
            col1, col2 = st.columns(2)
            with col1:
                st.success("Matched Skills")
                for skill in result["matched_skills"]:
                    st.write(f"✅ {skill}")
            with col2:
                st.warning("Missing Skills")
                for skill in result["missing_skills"]:
                    st.write(f"⚠️ {skill}")
            st.info("Improvement Suggestions")
            for recommendation in result["recommendations"]:
                st.write(f"• {recommendation}")
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
    job_description = st.text_area("Paste job offer here", height=260)
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
    uploaded_file = st.file_uploader("Upload CV as PDF", type=["pdf"])
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

elif menu == "Cover Letter Generator":
    st.markdown('<div class="section-title">Cover Letter Generator</div>', unsafe_allow_html=True)
    uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])
    job_description = st.text_area("Paste Job Description", height=250)
    resume_text = ""
    if uploaded_resume is not None:
        resume_text = extract_text_from_pdf(uploaded_resume)
        st.success("Resume uploaded successfully.")
    if st.button("Generate Cover Letter", use_container_width=True):
        if resume_text.strip() and job_description.strip():
            with st.spinner("Generating cover letter..."):
                cover_letter = generate_cover_letter(resume_text=resume_text, job_description=job_description)
            st.success("Cover letter generated successfully.")
            st.text_area("Generated Cover Letter", cover_letter, height=400)
        else:
            st.warning("Please upload a resume PDF and paste a job description.")

elif menu == "Client Communication Agent":
    st.markdown('<div class="section-title">Client Communication Agent</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Delay Message", "Progress Update", "Client Records"])
    with tab1:
        st.subheader("Delay Message Generator")
        client_options = clients["name"] + " - " + clients["service"]
        selected_client = st.selectbox("Select Client", client_options)
        client_index = client_options[client_options == selected_client].index[0]
        client = clients.loc[client_index]
        client_name = st.text_input("Client Name", value=client["name"])
        service_type = st.text_input("Service Type", value=client["service"])
        original_deadline = st.text_input("Original Deadline", value=client["deadline"])
        delay_reason = st.text_input("Delay Reason", value="Additional quality review")
        new_delivery_date = st.date_input("New Delivery Date")
        tone = st.selectbox("Tone", ["Professional", "Friendly", "Apologetic", "Formal", "Reassuring"])
        if st.button("Generate Delay Message", use_container_width=True):
            message = generate_client_delay_message(
                client_name=client_name,
                service_type=service_type,
                delay_reason=delay_reason,
                original_deadline=original_deadline,
                new_delivery_date=new_delivery_date,
                tone=tone
            )
            st.text_area("Generated Message", message, height=320)
    with tab2:
        st.subheader("Progress Update Generator")
        client_options_update = clients["name"] + " - " + clients["service"]
        selected_client_update = st.selectbox("Select Client for Update", client_options_update)
        client_index_update = client_options_update[client_options_update == selected_client_update].index[0]
        client_update = clients.loc[client_index_update]
        progress_client_name = st.text_input("Client Name", value=client_update["name"], key="progress_name")
        progress_service_type = st.text_input("Service Type", value=client_update["service"], key="progress_service")
        current_status = st.selectbox("Current Status", ["Pending", "In Progress", "Under Review", "Delayed", "Completed"])
        next_step = st.text_input("Next Step")
        progress_tone = st.selectbox("Tone", ["Professional", "Friendly", "Formal", "Reassuring"], key="progress_tone")
        if st.button("Generate Progress Update", use_container_width=True):
            if next_step.strip():
                message = generate_client_progress_update(
                    client_name=progress_client_name,
                    service_type=progress_service_type,
                    current_status=current_status,
                    next_step=next_step,
                    tone=progress_tone
                )
                st.text_area("Generated Update", message, height=320)
            else:
                st.warning("Please enter the next step.")
    with tab3:
        st.subheader("Client Records")
        st.dataframe(clients, use_container_width=True, hide_index=True)

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
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.write(user_question)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_assistant(user_question, candidates, jobs)
                st.write(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
