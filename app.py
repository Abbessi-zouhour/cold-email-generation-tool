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
    delete_candidate,
    add_client,
    update_client,
    delete_client
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
    candidates = get_candidates()
    jobs = get_jobs()
    clients = get_clients()

    total_candidates = len(candidates)
    total_jobs = len(jobs)
    total_clients = len(clients)

    available_candidates = len(candidates[candidates["status"].astype(str) == "Available"])
    placed_candidates = len(candidates[candidates["status"].astype(str) == "Placed"])

    open_jobs = len(jobs[jobs["status"].astype(str) == "Open"]) if "status" in jobs.columns else total_jobs

    pipeline_counts = candidates["pipeline_stage"].astype(str).value_counts()
    status_counts = candidates["status"].astype(str).value_counts()

    st.markdown("""
    <h1 class="hero-title">AI-powered <span>recruitment intelligence</span> platform</h1>
    <p class="hero-subtitle">
        Live recruitment dashboard powered by SQLite, online job search, AI analysis and candidate intelligence.
    </p>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat"><h2>{total_candidates}</h2><p>Total candidates</p></div>
        <div class="stat"><h2>{total_jobs}</h2><p>Total job offers</p></div>
        <div class="stat"><h2>{total_clients}</h2><p>Total clients</p></div>
        <div class="stat"><h2>{open_jobs}</h2><p>Open positions</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Recruitment overview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Candidates by status")
        if not status_counts.empty:
            st.bar_chart(status_counts)
        else:
            st.info("No candidate status data available.")

    with col2:
        st.markdown("#### Candidates by pipeline stage")
        if not pipeline_counts.empty:
            st.bar_chart(pipeline_counts)
        else:
            st.info("No pipeline data available.")

    st.markdown("### Quick insights")

    insight_col1, insight_col2, insight_col3 = st.columns(3)

    with insight_col1:
        st.markdown(f"""
        <div class="card">
            <h3>Available talent</h3>
            <p>{available_candidates} candidates are currently available for new opportunities.</p>
        </div>
        """, unsafe_allow_html=True)

    with insight_col2:
        st.markdown(f"""
        <div class="card">
            <h3>Placed candidates</h3>
            <p>{placed_candidates} candidates have already been placed or hired.</p>
        </div>
        """, unsafe_allow_html=True)

    with insight_col3:
        top_stage = pipeline_counts.index[0] if not pipeline_counts.empty else "No data"
        top_stage_count = pipeline_counts.iloc[0] if not pipeline_counts.empty else 0

        st.markdown(f"""
        <div class="card">
            <h3>Most active stage</h3>
            <p>{top_stage} has the highest number of candidates: {top_stage_count}.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Latest candidates")

    latest_candidates = candidates.tail(5).copy()

    st.dataframe(
        latest_candidates,
        width="stretch",
        hide_index=True
    )

    st.markdown("### Latest job opportunities")

    latest_jobs = jobs.tail(5).copy()

    display_job_cols = [
        col for col in [
            "company",
            "country",
            "job_title",
            "required_skills",
            "salary_range",
            "status",
            "job_link"
        ]
        if col in latest_jobs.columns
    ]

    st.dataframe(
        latest_jobs[display_job_cols],
        width="stretch",
        hide_index=True
    )
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
elif menu == "Candidate Pipeline":
    st.markdown(
        '<div class="section-eyebrow">PIPELINE</div>'
        '<h2 class="section-title">Candidate pipeline</h2>'
        '<p class="section-subtitle">Track candidates across the recruitment process.</p>',
        unsafe_allow_html=True
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
        stage_candidates = candidates[
            candidates["pipeline_stage"].astype(str) == stage
        ]

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
                skills = str(candidate.get("skills", ""))
                main_skill = skills.split(",")[0].strip() if skills else "Skill"

                pipeline_html += (
                    '<div class="candidate-card">'
                    f'<div class="candidate-name">{candidate.get("name", "")}</div>'
                    f'<div class="candidate-meta">{candidate.get("experience_years", 0)} years • {candidate.get("country", "")}</div>'
                    f'<span class="tag tag-python">{main_skill}</span>'
                    '</div>'
                )

        pipeline_html += '</div>'

    pipeline_html += '</div>'

    st.markdown(pipeline_html, unsafe_allow_html=True)
    

elif menu == "ATS Score":
    st.markdown('<div class="section-title">ATS Score Calculator</div>', unsafe_allow_html=True)

    st.caption("Search online jobs, select a target offer, upload a resume PDF, and calculate ATS compatibility.")

    ats_job_search = st.text_input(
        "Search online job",
        placeholder="Example: Python developer, English teacher, Data analyst..."
    )

    ats_country_options = {
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

    ats_selected_country = st.selectbox(
        "Online job country",
        list(ats_country_options.keys()),
        key="ats_country"
    )

    ats_country_code = ats_country_options[ats_selected_country]

    if st.button("Search online jobs for ATS", use_container_width=True):
        if ats_job_search.strip():
            with st.spinner("Fetching online jobs..."):
                st.session_state.ats_online_jobs = fetch_online_jobs(
                    search=ats_job_search,
                    country=ats_country_code
                )
        else:
            st.warning("Please enter a job title or keyword.")

    ats_jobs = st.session_state.get("ats_online_jobs", jobs.copy())

    if ats_jobs.empty:
        st.warning("No job offers available. Search online or add jobs to SQLite.")
    else:
        job_options = (
            ats_jobs["company"].astype(str)
            + " - "
            + ats_jobs["job_title"].astype(str)
            + " — ID "
            + ats_jobs["id"].astype(str)
        )

        selected_job = st.selectbox("Select target job", job_options)

        selected_job_id = int(float(selected_job.split("ID ")[1]))

        job = ats_jobs[
            ats_jobs["id"].astype(float).astype(int) == selected_job_id
        ].iloc[0]

        st.markdown(f"""
        <div class="card">
            <h3>{job['company']} - {job['job_title']}</h3>
            <p><b>Country:</b> {job['country']}</p>
            <p><b>Required Skills:</b> {job['required_skills']}</p>
            <p><b>Experience Required:</b> {job['experience_required']} years</p>
            <p><b>Language Required:</b> {job.get('language_required', 'Not specified')}</p>
            <p><b>Salary Range:</b> {job.get('salary_range', 'Not specified')}</p>
            <p><b>Job Link:</b> {job.get('job_link', '')}</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload resume PDF", type=["pdf"])

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
                        st.write(f"{skill}")

                with col2:
                    st.warning("Missing Skills")
                    for skill in result["missing_skills"]:
                        st.write(f"• {skill}")

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
    st.caption("Upload a resume PDF, search an online job offer, then generate a personalized application email.")

    if "email_jobs" not in st.session_state:
        st.session_state.email_jobs = pd.DataFrame()

    email_resume = st.file_uploader(
        "Upload resume PDF",
        type=["pdf"],
        key="email_resume_upload"
    )

    resume_text_for_email = ""

    if email_resume is not None:
        resume_text_for_email = extract_text_from_pdf(email_resume)
        st.success("Resume uploaded and extracted successfully.")

        with st.expander("Preview extracted resume text"):
            st.text_area(
                "Resume text",
                resume_text_for_email,
                height=220
            )

    candidate_name_email = st.text_input(
        "Candidate name",
        placeholder="Example: Amira Ben Ali"
    )

    email_job_search = st.text_input(
        "Search online job",
        placeholder="Example: English teacher, Python developer, Data analyst..."
    )

    email_country_options = {
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

    email_country_name = st.selectbox(
        "Online job country",
        list(email_country_options.keys()),
        key="email_job_country"
    )

    email_country_code = email_country_options[email_country_name]

    if st.button("Search online jobs", width="stretch"):
        if email_job_search.strip():
            with st.spinner("Searching online jobs..."):
                st.session_state.email_jobs = fetch_online_jobs(
                    search=email_job_search,
                    country=email_country_code
                )

            if st.session_state.email_jobs.empty:
                st.warning("No online jobs found. Try another keyword or country.")
            else:
                st.success(f"{len(st.session_state.email_jobs)} job offer(s) found.")
        else:
            st.warning("Please enter a job keyword first.")

    email_jobs = st.session_state.email_jobs.copy()

    if not email_jobs.empty:
        if "job_link" not in email_jobs.columns:
            email_jobs["job_link"] = ""

        job_options = (
            email_jobs["company"].astype(str)
            + " - "
            + email_jobs["job_title"].astype(str)
            + " — ID "
            + email_jobs["id"].astype(str)
        )

        selected_email_job = st.selectbox(
            "Select online job offer",
            job_options
        )

        selected_email_job_id = int(float(selected_email_job.split("ID ")[1]))

        selected_job_row = email_jobs[
            email_jobs["id"].astype(float).astype(int) == selected_email_job_id
        ].iloc[0]

        st.markdown(f"""
        <div class="card">
            <h3>{selected_job_row.get('company', '')} - {selected_job_row.get('job_title', '')}</h3>
            <p><b>Country / Location:</b> {selected_job_row.get('country', '')}</p>
            <p><b>Required skills / keyword:</b> {selected_job_row.get('required_skills', '')}</p>
            <p><b>Salary range:</b> {selected_job_row.get('salary_range', 'Not specified')}</p>
            <p><b>Job link:</b> {selected_job_row.get('job_link', '')}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Generate email", width="stretch"):
            if not resume_text_for_email.strip():
                st.warning("Please upload a resume PDF first.")
            elif not candidate_name_email.strip():
                st.warning("Please enter the candidate name.")
            else:
                required_skills_text = str(selected_job_row.get("required_skills", ""))
                resume_lower = resume_text_for_email.lower()

                skill_candidates = [
                    skill.strip()
                    for skill in required_skills_text.replace(";", ",").split(",")
                    if skill.strip()
                ]

                matched_skills = [
                    skill
                    for skill in skill_candidates
                    if skill.lower() in resume_lower
                ]

                if not matched_skills:
                    matched_skills = [required_skills_text] if required_skills_text else ["relevant experience"]

                with st.spinner("Generating personalized email..."):
                    email = generate_email(
                        candidate_name="Candidate from uploaded resume",
                        job_title=selected_job_row["job_title"],
                        company=selected_job_row["company"],
                        country=selected_job_row["country"],
                        matched_skills=selected_job_row["required_skills"]
                    )

                    email += f"""

                    Job offer link: {selected_job_row.get("job_link", "")}
                    """

                if isinstance(job_link, str) and job_link.strip():
                    email = f"{email}\n\nJob offer link: {job_link}"

                st.success("Email generated successfully.")
                st.text_area("Generated Email", email, height=360)
    else:
        st.info("Search for an online job offer to select it here.")

elif menu == "Job Analyzer":
    st.markdown('<div class="section-title">Job Offer Analyzer</div>', unsafe_allow_html=True)

    job_description = st.text_area("Paste job offer here", height=260)

    if st.button("Analyze Job Offer", use_container_width=True):
        if job_description.strip():
            with st.spinner("Analyzing job offer..."):
                result = analyze_job_offer(job_description)

            st.success("Analysis completed.")
            st.markdown(result)

            st.markdown("### Suggested candidates from database")

            job_text = job_description.lower()

            suggestions = []

            for _, candidate in candidates.iterrows():
                candidate_skills = str(candidate.get("skills", "")).lower()
                skill_list = [
                    skill.strip()
                    for skill in candidate_skills.replace(";", ",").split(",")
                    if skill.strip()
                ]

                matched_skills = [
                    skill for skill in skill_list
                    if skill in job_text
                ]

                if skill_list:
                    match_score = int((len(matched_skills) / len(skill_list)) * 100)
                else:
                    match_score = 0

                if matched_skills:
                    suggestions.append({
                        "candidate_name": candidate.get("name", ""),
                        "email": candidate.get("email", ""),
                        "country": candidate.get("country", ""),
                        "experience_years": candidate.get("experience_years", 0),
                        "skills": candidate.get("skills", ""),
                        "matched_skills": ", ".join(matched_skills),
                        "match_score": match_score
                    })

            if suggestions:
                suggestions_df = pd.DataFrame(suggestions)
                suggestions_df = suggestions_df.sort_values(
                    by="match_score",
                    ascending=False
                )

                st.dataframe(
                    suggestions_df,
                    width="stretch",
                    hide_index=True
                )

                chart_data = suggestions_df[
                    ["candidate_name", "match_score"]
                ].set_index("candidate_name")

                st.bar_chart(chart_data)
            else:
                st.warning("No matching candidates found in the database.")
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

    clients = get_clients()

    tab1, tab2, tab3, tab4 = st.tabs([
        "Delay Message",
        "Progress Update",
        "Client Records",
        "Manage Clients"
    ])

    with tab1:
        st.subheader("Delay Message Generator")

        if clients.empty:
            st.warning("No clients found. Add a client from Manage Clients first.")
        else:
            client_options = clients["name"].astype(str) + " - " + clients["service"].astype(str)
            selected_client = st.selectbox("Select Client", client_options)

            client_index = client_options[client_options == selected_client].index[0]
            client = clients.loc[client_index]

            client_name = st.text_input("Client Name", value=str(client["name"]))
            service_type = st.text_input("Service Type", value=str(client["service"]))
            original_deadline = st.text_input("Original Deadline", value=str(client["deadline"]))
            delay_reason = st.text_input("Delay Reason", value="Additional quality review")
            new_delivery_date = st.date_input("New Delivery Date")
            tone = st.selectbox("Tone", ["Professional", "Friendly", "Apologetic", "Formal", "Reassuring"])

            if st.button("Generate Delay Message", width="stretch"):
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

        if clients.empty:
            st.warning("No clients found. Add a client from Manage Clients first.")
        else:
            client_options_update = clients["name"].astype(str) + " - " + clients["service"].astype(str)
            selected_client_update = st.selectbox("Select Client for Update", client_options_update)

            client_index_update = client_options_update[client_options_update == selected_client_update].index[0]
            client_update = clients.loc[client_index_update]

            progress_client_name = st.text_input("Client Name", value=str(client_update["name"]), key="progress_name")
            progress_service_type = st.text_input("Service Type", value=str(client_update["service"]), key="progress_service")

            current_status = st.selectbox(
                "Current Status",
                ["Pending", "In Progress", "Under Review", "Delayed", "Completed"]
            )

            next_step = st.text_input("Next Step")
            progress_tone = st.selectbox(
                "Tone",
                ["Professional", "Friendly", "Formal", "Reassuring"],
                key="progress_tone"
            )

            if st.button("Generate Progress Update", width="stretch"):
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

        clients = get_clients()

        st.dataframe(
            clients,
            width="stretch",
            hide_index=True
        )

    with tab4:
        st.subheader("Manage clients")

        clients = get_clients()

        action = st.selectbox(
            "Action",
            ["Add client", "Edit client", "Delete client"]
        )

        if action == "Add client":
            name = st.text_input("Client name")
            service = st.text_input("Service")
            deadline = st.date_input("Deadline")
            status = st.selectbox("Status", ["Pending", "In Progress", "Delayed", "Completed"])

            if st.button("Save client"):
                if name.strip() and service.strip():
                    add_client(name, service, str(deadline), status)
                    st.success("Client added successfully.")
                    st.rerun()
                else:
                    st.warning("Client name and service are required.")

        elif action == "Edit client":
            if clients.empty:
                st.warning("No clients available to edit.")
            else:
                candidate_options = candidates["name"].astype(str) + " — ID " + candidates["id"].astype(str)

                selected_candidate_client = st.selectbox(
                    "Select candidate",
                    candidate_options
                )

                candidate_id = int(float(selected_candidate_client.split("ID ")[1]))

                candidate_client = candidates[
                    candidates["id"].astype(float).astype(int) == candidate_id
                ].iloc[0]

                client_name = st.text_input("Client Name", value=str(candidate_client["name"]))
                service_type = st.text_input("Service Type", value="Recruitment / Job application support")
                original_deadline = st.text_input("Original Deadline", value="")

                status_options = ["Pending", "In Progress", "Delayed", "Completed"]

                edit_status = st.selectbox(
                    "Status",
                    status_options,
                    index=status_options.index(client_row["status"])
                    if str(client_row["status"]) in status_options else 0
                )

                if st.button("Update client"):
                    update_client(client_id, edit_name, edit_service, edit_deadline, edit_status)
                    st.success("Client updated successfully.")
                    st.rerun()

        elif action == "Delete client":
            if clients.empty:
                st.warning("No clients available to delete.")
            else:
                client_options = clients["name"].astype(str) + " — ID " + clients["id"].astype(str)
                selected_client = st.selectbox("Select client to delete", client_options)

                client_id = int(float(selected_client.split("ID ")[1]))

                confirm = st.checkbox("I confirm delete")

                if st.button("Delete client"):
                    if confirm:
                        delete_client(client_id)
                        st.success("Client deleted successfully.")
                        st.rerun()
                    else:
                        st.warning("Please confirm first.")
    
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