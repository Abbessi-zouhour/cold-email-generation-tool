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
from services.job_api import fetch_online_jobs
from services.assistant_agent import ask_assistant

from database_manager import (
    get_candidates,
    get_jobs,
    get_clients,
    add_candidate,
    update_candidate,
    delete_candidate
)


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

country_options = {
    "United Kingdom": "gb",
    "France": "fr",
    "Canada": "ca",
    "United States": "us",
    "Germany": "de",
    "Netherlands": "nl",
    "Belgium": "be",
    "Australia": "au",
    "Italy": "it",
    "Spain": "es",
    "India": "in",
    "Singapore": "sg",
    "New Zealand": "nz",
    "South Africa": "za"
}

selected_job_country = st.sidebar.selectbox(
    "Online search country",
    list(country_options.keys())
)

job_country = country_options[selected_job_country]

use_online_jobs = st.sidebar.button("Fetch Online Jobs")


# SQLite loading
if uploaded_candidates is not None:
    candidates = pd.read_csv(uploaded_candidates)
else:
    candidates = get_candidates()

if use_online_jobs:
    jobs = fetch_online_jobs(
        search=job_search_keyword,
        country=job_country
    )
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

    st.caption("Search jobs by title, keyword or profession. Use online search to fetch fresh jobs from Adzuna / fallback APIs.")

    job_country_options = {
        "United Kingdom": "gb",
        "France": "fr",
        "Canada": "ca",
        "United States": "us",
        "Germany": "de",
        "Netherlands": "nl",
        "Belgium": "be",
        "Australia": "au",
        "Italy": "it",
        "Spain": "es",
        "India": "in",
        "Singapore": "sg",
        "New Zealand": "nz",
        "South Africa": "za"
    }

    search_job = st.text_input(
        "Search jobs online",
        value=job_search_keyword if use_online_jobs else "",
        placeholder="Example: English teacher, Python developer, Data analyst..."
    )

    selected_country_name = st.selectbox(
        "Online search country",
        list(job_country_options.keys()),
        index=list(job_country_options.keys()).index(selected_job_country)
        if selected_job_country in job_country_options else 0
    )

    selected_country_code = job_country_options[selected_country_name]

    col_search, col_reset = st.columns([1, 1])

    with col_search:
        search_online_clicked = st.button("Search Online Jobs", use_container_width=True)

    with col_reset:
        show_local_clicked = st.button("Show Local SQLite Jobs", use_container_width=True)

    if search_online_clicked and search_job.strip():
        with st.spinner("Fetching online job offers..."):
            filtered_jobs = fetch_online_jobs(
                search=search_job,
                country=selected_country_code
            )

        if filtered_jobs.empty:
            st.warning("No online jobs found for this search. Try another keyword or country.")
    elif use_online_jobs:
        filtered_jobs = jobs.copy()
    elif show_local_clicked or not search_job.strip():
        filtered_jobs = jobs.copy()
    else:
        search_text = search_job.lower()

        filtered_jobs = jobs[
            jobs["job_title"].astype(str).str.lower().str.contains(search_text, na=False)
            |
            jobs["required_skills"].astype(str).str.lower().str.contains(search_text, na=False)
            |
            jobs["company"].astype(str).str.lower().str.contains(search_text, na=False)
        ]

    if "job_link" not in filtered_jobs.columns:
        filtered_jobs["job_link"] = ""

    st.markdown(f"**{len(filtered_jobs)} job offer(s) found**")

    display_columns = [
        col for col in [
            "id",
            "company",
            "country",
            "job_title",
            "required_skills",
            "experience_required",
            "language_required",
            "salary_range",
            "status",
            "job_link"
        ]
        if col in filtered_jobs.columns
    ]

    st.dataframe(
        filtered_jobs[display_columns],
        width="stretch",
        hide_index=True
    )

    if not filtered_jobs.empty and "job_link" in filtered_jobs.columns:
        st.markdown("### Apply links")

        for _, row in filtered_jobs.head(20).iterrows():
            job_title = row.get("job_title", "Job offer")
            company = row.get("company", "Company")
            link = row.get("job_link", "")

            if isinstance(link, str) and link.strip():
                st.markdown(f"- [{job_title} — {company}]({link})")
            else:
                st.markdown(f"- {job_title} — {company} *(no link available)*")


elif menu == "Candidates":
    st.markdown('<div class="section-title">Candidates</div>', unsafe_allow_html=True)

    tab_add, tab_edit, tab_delete, tab_view = st.tabs([
        "Add candidate",
        "Edit candidate",
        "Delete candidate",
        "View candidates"
    ])

    with tab_add:
        st.subheader("Add new candidate")

        with st.form("add_candidate_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            country = st.text_input("Country")
            experience_years = st.number_input("Experience years", min_value=0, max_value=50, value=0)
            skills = st.text_area("Skills")

            status = st.selectbox(
                "Status",
                ["Available", "Placed", "In Process", "Interviewing"]
            )

            pipeline_stage = st.selectbox(
                "Pipeline stage",
                ["Applied", "Screening", "Interview Scheduled", "Client Review", "Offer Sent", "Hired", "Rejected"]
            )

            submitted = st.form_submit_button("Save candidate")

            if submitted:
                if name.strip() and email.strip():
                    add_candidate(name, email, country, experience_years, skills, status, pipeline_stage)
                    st.success("Candidate saved successfully.")
                    st.rerun()
                else:
                    st.warning("Name and email are required.")

    with tab_edit:
        st.subheader("Edit candidate")

        candidate_options = candidates["name"] + " — ID " + candidates["id"].astype(str)

        selected_candidate = st.selectbox(
            "Select candidate to edit",
            candidate_options
        )

        selected_id = int(float(selected_candidate.split("ID ")[1]))
        candidate_row = candidates[candidates["id"] == selected_id].iloc[0]

        with st.form("edit_candidate_form"):
            edit_name = st.text_input("Name", value=candidate_row["name"])
            edit_email = st.text_input("Email", value=candidate_row["email"])
            edit_country = st.text_input("Country", value=candidate_row["country"])

            edit_experience = st.number_input(
                "Experience years",
                min_value=0,
                max_value=50,
                value=int(candidate_row["experience_years"])
            )

            edit_skills = st.text_area("Skills", value=candidate_row["skills"])

            edit_status = st.selectbox(
                "Status",
                ["Available", "Placed", "In Process", "Interviewing"],
                index=["Available", "Placed", "In Process", "Interviewing"].index(candidate_row["status"])
                if candidate_row["status"] in ["Available", "Placed", "In Process", "Interviewing"] else 0
            )

            edit_pipeline_stage = st.selectbox(
                "Pipeline stage",
                ["Applied", "Screening", "Interview Scheduled", "Client Review", "Offer Sent", "Hired", "Rejected"],
                index=["Applied", "Screening", "Interview Scheduled", "Client Review", "Offer Sent", "Hired", "Rejected"].index(candidate_row["pipeline_stage"])
                if candidate_row["pipeline_stage"] in ["Applied", "Screening", "Interview Scheduled", "Client Review", "Offer Sent", "Hired", "Rejected"] else 0
            )

            update_submitted = st.form_submit_button("Update candidate")

            if update_submitted:
                update_candidate(
                    selected_id,
                    edit_name,
                    edit_email,
                    edit_country,
                    edit_experience,
                    edit_skills,
                    edit_status,
                    edit_pipeline_stage
                )

                st.success("Candidate updated successfully.")
                st.rerun()

    with tab_delete:
        st.subheader("Delete candidate")

        delete_options = candidates["name"] + " — ID " + candidates["id"].astype(str)

        selected_delete = st.selectbox(
            "Select candidate to delete",
            delete_options
        )

        delete_id = int(float(selected_delete.split("ID ")[1]))

        confirm_delete = st.checkbox("I confirm I want to delete this candidate")

        if st.button("Delete candidate"):
            if confirm_delete:
                delete_candidate(delete_id)
                st.success("Candidate deleted successfully.")
                st.rerun()
            else:
                st.warning("Please confirm before deleting.")

    with tab_view:
        st.subheader("Candidate database")

        status_filter = st.selectbox(
            "Filter by status",
            ["All"] + sorted(candidates["status"].unique().tolist())
        )

        filtered_candidates = candidates.copy()

        if status_filter != "All":
            filtered_candidates = filtered_candidates[
                filtered_candidates["status"] == status_filter
            ]

        st.dataframe(
            filtered_candidates,
            use_container_width=True,
            hide_index=True
        )
    stages = [
        "Applied",
        "Screening",
        "Interview Scheduled",
        "Client Review",
        "Offer Sent",
        "Hired",
        "Rejected"
    ]

    pipeline_html = '<div class="kanban-board">'

    for stage in stages:
        stage_candidates = candidates[candidates["pipeline_stage"] == stage]

        pipeline_html += (
            '<div class="kanban-column">'
            '<div class="kanban-header">'
            f'<span>{stage}</span>'
            f'<span class="count-badge">{len(stage_candidates)}</span>'
            '</div>'
        )

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

                pipeline_html += (
                    '<div class="candidate-card">'
                    f'<div class="candidate-name">{candidate["name"]}</div>'
                    f'<div class="candidate-meta">{candidate["experience_years"]} years • {candidate["country"]}</div>'
                    f'<span class="tag {skill_class}">{main_skill}</span>'
                    '</div>'
                )

        pipeline_html += '</div>'

    pipeline_html += '</div>'

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
            result = calculate_ats_score(
                cv_text=cv_text,
                job_skills=job["required_skills"]
            )

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
                    st.write(f" {skill}")

            st.info("Improvement Suggestions")
            for recommendation in result["recommendations"]:
                st.write(f"• {recommendation}")
        else:
            st.warning("Please upload a resume PDF first.")

elif menu == "Candidate Matching":
    st.markdown('<div class="section-title">Candidate Matching</div>', unsafe_allow_html=True)

    search_job_match = st.text_input(
        "Search job by name or title",
        placeholder="Example: Software Engineer, Python Developer, Teacher..."
    )

    search_matching_online = st.button("Search online job offers for matching")

    if search_matching_online and search_job_match.strip():
        jobs_for_matching = fetch_online_jobs(
            search=search_job_match,
            country=job_country
        )
    else:
        jobs_for_matching = jobs.copy()

        if search_job_match.strip():
            search_text = search_job_match.lower()

            jobs_for_matching = jobs_for_matching[
                jobs_for_matching["job_title"].astype(str).str.lower().str.contains(search_text, na=False)
                |
                jobs_for_matching["company"].astype(str).str.lower().str.contains(search_text, na=False)
                |
                jobs_for_matching["required_skills"].astype(str).str.lower().str.contains(search_text, na=False)
            ]

    if jobs_for_matching.empty:
        st.warning("No job offers found. Try another keyword or use online search.")
    else:
        job_options = (
            jobs_for_matching["company"].astype(str)
            + " - "
            + jobs_for_matching["job_title"].astype(str)
            + " — ID "
            + jobs_for_matching["id"].astype(str)
        )

        selected_job = st.selectbox("Select Job Offer", job_options)

        selected_job_id = int(float(selected_job.split("ID ")[1]))

        job = jobs_for_matching[
            jobs_for_matching["id"].astype(float).astype(int) == selected_job_id
        ].iloc[0]

        job, matches = match_candidates(
            selected_job_id,
            candidates,
            jobs_for_matching
        )

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

        if matches.empty:
            st.warning("No matching candidates found.")
        else:
            st.dataframe(matches, width="stretch", hide_index=True)

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
                cover_letter = generate_cover_letter(
                    resume_text=resume_text,
                    job_description=job_description
                )

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