import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image
from datetime import date


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
from services.recommendation_engine import recommend_candidates
from services.interview_questions import generate_interview_questions
from services.interview_email import generate_interview_invitation_email
from services.email_sender import send_email
from services.pipeline_manager import update_candidate_stage
from services.interview_scorecard import evaluate_candidate
from database_manager import (
    get_candidates,
    get_jobs,
    get_clients,
    get_candidate_by_id,
    add_candidate,
    update_candidate,
    delete_candidate,

)
from services.user_manager import (
    get_user,
    update_password,
    get_all_users,
    create_user,
    update_user,
    delete_user,
    username_exists
)

from services.interview_scheduler import (
    add_interview,
    get_interviews,
    delete_interview
)
from services.analytics_dashboard import (
    calculate_dashboard_metrics,
    get_pipeline_counts,
    get_status_counts,
    get_country_counts,
    get_jobs_by_country,
    get_interviews_by_status
)
from services.candidate_timeline import *
from services.supabase_manager import (
    add_interview_supabase,
    delete_interview_supabase,
    get_interviews_supabase,
    update_candidate_stage_supabase,
    add_timeline_event_supabase,
    get_candidates_supabase,
)

from services.supabase_manager import (
    get_candidates_supabase,
    get_jobs_supabase,
    get_clients_supabase,
    get_interviews_supabase,
    get_candidate_by_id_supabase,
    add_candidate_supabase,
    update_candidate_stage_supabase,
    add_timeline_event_supabase,
    get_candidate_timeline_supabase,

    add_client_supabase,
    update_client_supabase,
    delete_client_supabase
)
from services.supabase_client import supabase
from services.auth import login

from services.candidate_notes import (
    get_candidate_notes,
    add_candidate_note,
    delete_candidate_note
)

BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "assets" / "images" / "logo.png"

logo_icon = Image.open(LOGO_PATH) if LOGO_PATH.exists() else "TB"

st.set_page_config(
    page_title="TalentBridge",
    page_icon=logo_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)
if not login(LOGO_PATH if LOGO_PATH.exists() else None):
    st.stop()


def load_css():
    css_path = BASE_DIR / "assets" / "main.css"
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


ROLE_PERMISSIONS = {
    "Admin": [
        "Dashboard",
        "Job Offers",
        "Candidates",
        "Candidate Profile",
        "Candidate Matching",
        "Candidate Pipeline",
        "Candidate Timeline",
        "Interview Scheduler",
        "AI Interview Questions",
        "Interview Scorecard",
        "Email Generator",
        "Job Analyzer",
        "CV Parser",
        "ATS Score",
        "Cover Letter Generator",
        "Client Communication Agent",
        "AI Assistant"
    ],
    "Recruiter": [
        "Dashboard",
        "Job Offers",
        "Candidates",
        "Candidate Profile",
        "Candidate Matching",
        "Candidate Pipeline",
        "Candidate Timeline",
        "Interview Scheduler",
        "Email Generator",
        "AI Assistant"
    ],
    "Manager": [
        "Dashboard",
        "Candidate Matching",
        "Candidate Pipeline",
        "Interview Scorecard",
        "Client Communication Agent"
    ]
}

user_role = st.session_state.get("role", "Recruiter")

menu_options = ROLE_PERMISSIONS.get(user_role, ROLE_PERMISSIONS["Recruiter"])

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# Sidebar
if LOGO_PATH.exists():
    st.sidebar.image(str(LOGO_PATH), use_container_width=True)

st.sidebar.markdown(
    "<div class='sidebar-subtitle'>Recruitment Intelligence Platform</div>",
    unsafe_allow_html=True
)

current_page = (
    st.session_state.page
    if st.session_state.page in menu_options
    else "Dashboard"
)

menu = st.sidebar.radio(
    "Navigation",
    menu_options,
    index=menu_options.index(current_page)
)

if st.session_state.page in menu_options:
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

username = st.session_state.get("username", "User")
role = st.session_state.get("role", "User")

st.sidebar.markdown(
    f"""
    <div class="sidebar-user-card">
        <div class="sidebar-user-name"> {username}</div>
        <div class="sidebar-user-role">Role: {role}</div>
    </div>
    """,
    unsafe_allow_html=True
)

if st.sidebar.button("Settings", use_container_width=True):
    st.session_state.page = "Settings"
    st.rerun()

if st.sidebar.button("Logout", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.page = "Dashboard"
    st.rerun()

if st.session_state.page not in menu_options and st.session_state.page != "Settings":
    st.warning("You do not have permission to access this page.")
    st.session_state.page = "Dashboard"
    st.rerun()
# SQLite loading
if uploaded_candidates is not None:
    candidates = pd.read_csv(uploaded_candidates)
else:
    candidates = get_candidates_supabase()

if use_online_jobs:
    jobs = fetch_online_jobs(
        search=job_search_keyword,
        country=job_country
    )
elif uploaded_jobs is not None:
    jobs = pd.read_csv(uploaded_jobs)
else:
    jobs = get_jobs_supabase()

if uploaded_clients is not None:
    clients = pd.read_csv(uploaded_clients)
else:
    clients = get_clients_supabase()


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
    candidates = get_candidates_supabase()
    jobs = get_jobs_supabase()
    clients = get_clients_supabase()
    interviews = get_interviews_supabase()

    metrics = calculate_dashboard_metrics(
        candidates,
        jobs,
        clients,
        interviews
    )

    pipeline_counts = get_pipeline_counts(candidates)
    status_counts = get_status_counts(candidates)
    country_counts = get_country_counts(candidates)
    jobs_country_counts = get_jobs_by_country(jobs)
    interview_status_counts = get_interviews_by_status(interviews)

    st.markdown("""
    <h1 class="hero-title">AI-powered <span>recruitment intelligence</span> platform</h1>
    <p class="hero-subtitle">
        Live recruitment dashboard, online job search, AI analysis and candidate intelligence.
    </p>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat"><h2>{metrics["total_candidates"]}</h2><p>Total candidates</p></div>
        <div class="stat"><h2>{metrics["total_jobs"]}</h2><p>Total job offers</p></div>
        <div class="stat"><h2>{metrics["total_clients"]}</h2><p>Total clients</p></div>
        <div class="stat"><h2>{metrics["total_interviews"]}</h2><p>Scheduled interviews</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat"><h2>{metrics["open_jobs"]}</h2><p>Open positions</p></div>
        <div class="stat"><h2>{metrics["available_candidates"]}</h2><p>Available candidates</p></div>
        <div class="stat"><h2>{metrics["hired_candidates"]}</h2><p>Hired candidates</p></div>
        <div class="stat"><h2>{metrics["hiring_rate"]}%</h2><p>Hiring rate</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Analytics charts")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Pipeline distribution")
        if pipeline_counts is not None and not pipeline_counts.empty:
            st.bar_chart(pipeline_counts)
        else:
            st.info("No pipeline data available.")

    with col2:
        st.markdown("#### Candidates by status")
        if status_counts is not None and not status_counts.empty:
            st.bar_chart(status_counts)
        else:
            st.info("No status data available.")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### Candidates by country")
        if country_counts is not None and not country_counts.empty:
            st.bar_chart(country_counts)
        else:
            st.info("No country data available.")

    with col4:
        st.markdown("#### Jobs by country")
        if jobs_country_counts is not None and not jobs_country_counts.empty:
            st.bar_chart(jobs_country_counts)
        else:
            st.info("No job country data available.")

    st.markdown("#### Interviews by status")

    if interview_status_counts is not None and not interview_status_counts.empty:
        st.bar_chart(interview_status_counts)
    else:
        st.info("No interview status data yet.")

    st.markdown("### Quick insights")

    insight_col1, insight_col2, insight_col3 = st.columns(3)

    with insight_col1:
        st.markdown(f"""
        <div class="card">
            <h3>Available talent</h3>
            <p>{metrics["available_candidates"]} candidates are currently available for new opportunities.</p>
        </div>
        """, unsafe_allow_html=True)

    with insight_col2:
        st.markdown(f"""
        <div class="card">
            <h3>Interview activity</h3>
            <p>{metrics["total_interviews"]} interviews are currently scheduled in the system.</p>
        </div>
        """, unsafe_allow_html=True)

    with insight_col3:
        top_stage = pipeline_counts.index[0] if pipeline_counts is not None and not pipeline_counts.empty else "No data"
        top_stage_count = pipeline_counts.iloc[0] if pipeline_counts is not None and not pipeline_counts.empty else 0

        st.markdown(f"""
        <div class="card">
            <h3>Most active stage</h3>
            <p>{top_stage} has the highest number of candidates: {top_stage_count}.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Latest candidates")

    if not candidates.empty:
        st.dataframe(
            candidates.tail(5),
            width="stretch",
            hide_index=True
        )
    else:
        st.info("No candidates available.")

    st.markdown("### Latest job opportunities")

    if not jobs.empty:
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
            if col in jobs.columns
        ]

        st.dataframe(
            jobs[display_job_cols].tail(5),
            width="stretch",
            hide_index=True
        )
    else:
        st.info("No jobs available.")

    st.markdown("### Upcoming interviews")

    if not interviews.empty:
        st.dataframe(
            interviews.tail(5),
            width="stretch",
            hide_index=True
        )
    else:
        st.info("No interviews scheduled.")
    st.write("Supabase candidates test")
    st.dataframe(get_candidates_supabase().head())
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
        search_online_clicked = st.button("Search Online Jobs", width="stretch")

    with col_reset:
        show_local_clicked = st.button("Show Local Jobs", width="stretch")

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

    if not filtered_jobs.empty:
        st.markdown("### Automatic Candidate Recommendations")

        job_options = (
            filtered_jobs["company"].astype(str)
            + " - "
            + filtered_jobs["job_title"].astype(str)
            + " — ID "
            + filtered_jobs["id"].astype(str)
        )

        selected_recommendation_job = st.selectbox(
            "Select job to recommend candidates",
            job_options
        )

        selected_recommendation_id = selected_recommendation_job.split("ID ")[1]

        selected_job_row = filtered_jobs[
            filtered_jobs["id"].astype(str) == selected_recommendation_id
        ].iloc[0]

        recommendations_df = recommend_candidates(
            selected_job_row,
            candidates
        )

        if not recommendations_df.empty:
            st.dataframe(
                recommendations_df,
                width="stretch",
                hide_index=True
            )
        else:
            st.info("No matching candidates found for this job.")

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

    candidates = get_candidates_supabase()

    st.write("Candidates loaded:", len(candidates))

    if candidates.empty:
        st.warning("No candidates found.")
    else:
        st.dataframe(
            candidates,
            use_container_width=True,
            hide_index=True
        )
elif menu == "Candidate Profile":
    st.markdown('<div class="section-title">Candidate Profile</div>', unsafe_allow_html=True)

    candidates = get_candidates_supabase()

    if candidates.empty:
        st.warning("No candidates found in Supabase.")

    elif "id" not in candidates.columns or "name" not in candidates.columns:
        st.error("Supabase candidates table must contain 'id' and 'name' columns.")
        st.write("Current columns:", list(candidates.columns))

    else:
        candidates = candidates.dropna(subset=["id", "name"])
        candidates = candidates[candidates["name"].astype(str).str.lower() != "nan"]

        if candidates.empty:
            st.warning("No valid candidates found.")

        else:
            candidate_options = (
                candidates["name"].astype(str)
                + " — ID "
                + candidates["id"].astype(float).astype(int).astype(str)
            ).tolist()

            selected_candidate = st.selectbox(
                "Select candidate",
                candidate_options,
                key="profile_selected_candidate"
            )

            candidate_id = int(float(selected_candidate.split("ID ")[1]))

            candidate_df = get_candidate_by_id_supabase(candidate_id)

            if candidate_df.empty:
                st.warning("Candidate not found.")

            else:
                candidate = candidate_df.iloc[0]

                st.markdown(f"""
                <div class="card">
                    <h2>{candidate.get("name", "")}</h2>
                    <p><b>Email:</b> {candidate.get("email", "")}</p>
                    <p><b>Phone:</b> {candidate.get("phone", "")}</p>
                    <p><b>Country:</b> {candidate.get("country", "")}</p>
                    <p><b>Experience:</b> {candidate.get("experience_years", 0)} years</p>
                    <p><b>Languages:</b> {candidate.get("languages", "")}</p>
                    <p><b>Status:</b> {candidate.get("status", "")}</p>
                    <p><b>Pipeline stage:</b> {candidate.get("pipeline_stage", "")}</p>
                    <p><b>Skills:</b> {candidate.get("skills", "")}</p>
                </div>
                """, unsafe_allow_html=True)

                st.divider()

                st.subheader("Candidate Notes")

                new_note = st.text_area(
                    "Add note",
                    key=f"note_text_{candidate_id}",
                    placeholder="Write a note about this candidate..."
                )

                if st.button(
                    "Save Note",
                    use_container_width=True,
                    key=f"save_note_{candidate_id}"
                ):
                    if not new_note.strip():
                        st.warning("Please write a note first.")
                    else:
                        add_candidate_note(
                            candidate_id=candidate_id,
                            note=new_note,
                            created_by=st.session_state.get("username", "Unknown")
                        )

                        st.success("Note saved successfully.")
                        st.rerun()

                notes = get_candidate_notes(candidate_id)

                if notes:
                    st.markdown("### Notes History")

                    for note in notes:
                        st.markdown(
                            f"""
                            <div class="card" style="margin-bottom:12px;">
                                <p>{note.get("note", "")}</p>
                                <p style="font-size:13px;color:#6B7280;">
                                    By {note.get("created_by", "Unknown")}
                                    · {note.get("created_at", "")}
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        if st.button(
                            "Delete Note",
                            key=f"delete_note_{note['id']}"
                        ):
                            delete_candidate_note(note["id"])
                            st.success("Note deleted.")
                            st.rerun()

                else:
                    st.info("No notes yet for this candidate.")

elif menu == "Candidate Pipeline":
    st.markdown(
        '<div class="section-eyebrow">PIPELINE</div>'
        '<h2 class="section-title">Candidate pipeline</h2>'
        '<p class="section-subtitle">Track and update candidates across the recruitment process.</p>',
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

    candidates = get_candidates_supabase()

    if candidates.empty:
        st.warning("No candidates found.")
        st.stop()

    candidates = candidates.dropna(subset=["id", "name"])

    candidate_ids = candidates["id"].astype(int).tolist()

    selected_id = st.selectbox(
        "Select candidate",
        candidate_ids,
        format_func=lambda x: (
            candidates[candidates["id"].astype(int) == x].iloc[0]["name"]
            + " — "
            + str(candidates[candidates["id"].astype(int) == x].iloc[0]["pipeline_stage"])
            + f" — ID {x}"
        )
    )

    candidate_row = candidates[
        candidates["id"].astype(int) == int(selected_id)
    ].iloc[0]

    current_stage = str(candidate_row.get("pipeline_stage", "Applied"))

    new_stage = st.selectbox(
        "Move to stage",
        stages,
        index=stages.index(current_stage) if current_stage in stages else 0
    )

    if st.button("Update candidate stage", width="stretch"):
        update_candidate_stage_supabase(int(selected_id), new_stage)

        add_timeline_event_supabase(
            candidate_id=int(selected_id),
            event_date=date.today(),
            event_type=f"Moved to {new_stage}",
            notes=f"Candidate moved from {current_stage} to {new_stage}."
        )

        st.success(f"{candidate_row.get('name', '')} moved to {new_stage}.")
        st.rerun()

    st.markdown("### Pipeline board")

    refreshed_candidates = get_candidates_supabase()

    pipeline_html = '<div class="kanban-board">'

    for stage in stages:
        stage_candidates = refreshed_candidates[
            refreshed_candidates["pipeline_stage"].astype(str) == stage
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

    st.markdown(
        '<div class="section-title">Candidate Timeline</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Track every interaction and milestone for each candidate."
    )

    valid_candidates = candidates.dropna(
        subset=["id", "name"]
    )

    if valid_candidates.empty:

        st.warning("No candidates available.")

    else:

        candidate_options = (
            valid_candidates["name"].astype(str)
            + " — ID "
            + valid_candidates["id"].astype(float).astype(int).astype(str)
        )

        selected_candidate = st.selectbox(
            "Select candidate",
            candidate_options
        )

        candidate_id = int(
            selected_candidate.split("ID ")[1]
        )

        candidate_row = valid_candidates[
            valid_candidates["id"].astype(float).astype(int)
            == candidate_id
        ].iloc[0]

        st.markdown("### Candidate Information")

        st.info(
            f"""
Name: {candidate_row.get('name','')}

Email: {candidate_row.get('email','')}

Country: {candidate_row.get('country','')}

Experience: {candidate_row.get('experience_years',0)} years

Skills: {candidate_row.get('skills','')}

Current Stage: {candidate_row.get('pipeline_stage','')}
"""
        )

        st.markdown("### Add Timeline Event")

        event_date = st.date_input(
            "Event Date"
        )

        event_type = st.selectbox(
            "Event Type",
            [
                "Applied",
                "Screening",
                "Phone Interview",
                "Technical Interview",
                "HR Interview",
                "Client Review",
                "Offer Sent",
                "Offer Accepted",
                "Offer Rejected",
                "Hired",
                "Rejected"
            ]
        )

        notes = st.text_area(
            "Notes",
            placeholder="Add recruiter notes..."
        )

        if st.button(
            "Add Timeline Event",
            width="stretch"
        ):

            add_timeline_event(
                candidate_id=candidate_id,
                event_date=str(event_date),
                event_type=event_type,
                notes=notes
            )

            st.success(
                "Timeline event added successfully."
            )

            st.rerun()

        st.markdown("### Candidate Timeline")

        timeline = get_candidate_timeline(
            candidate_id
        )

        if timeline.empty:

            st.info(
                "No timeline events recorded yet."
            )

        else:

            for _, row in timeline.iterrows():

                st.markdown(
                    f"""
<div class="card">
<h3>{row['event_type']}</h3>
<p><b>Date:</b> {row['event_date']}</p>
<p>{row['notes']}</p>
</div>
""",
                    unsafe_allow_html=True
                )

            st.dataframe(
                timeline,
                width="stretch",
                hide_index=True
            )

            st.markdown("### Delete Timeline Event")

            event_options = (
                timeline["event_type"].astype(str)
                + " — "
                + timeline["event_date"].astype(str)
                + " — ID "
                + timeline["id"].astype(str)
            )

            selected_event = st.selectbox(
                "Select event to delete",
                event_options
            )

            event_id = int(
                float(
                    selected_event.split("ID ")[1]
                )
            )

            confirm_delete = st.checkbox(
                "I confirm delete this event"
            )

            if st.button(
                "Delete Timeline Event",
                width="stretch"
            ):

                if confirm_delete:

                    delete_timeline_event(
                        event_id
                    )

                    st.success(
                        "Timeline event deleted successfully."
                    )

                    st.rerun()

                else:

                    st.warning(
                        "Please confirm deletion first."
                    )
elif menu == "Candidate Timeline":
    st.markdown('<div class="section-title">Candidate Timeline</div>', unsafe_allow_html=True)

    candidates = get_candidates_supabase()

    if candidates.empty or "id" not in candidates.columns or "name" not in candidates.columns:
        st.warning("No valid candidates found from Supabase.")
        st.stop()

    valid_candidates = candidates.dropna(subset=["id", "name"])

    candidate_options = (
        valid_candidates["name"].astype(str)
        + " — ID "
        + valid_candidates["id"].astype(float).astype(int).astype(str)
    )

    selected_candidate = st.selectbox(
        "Select candidate",
        candidate_options,
        key="timeline_candidate_select"
    )

    candidate_id = int(float(selected_candidate.split("ID ")[1]))

    st.markdown("### Add timeline event")

    event_date = st.date_input("Event date", value=date.today())
    event_type = st.selectbox(
        "Event type",
        [
            "Applied",
            "Screening",
            "Interview Scheduled",
            "Client Review",
            "Offer Sent",
            "Hired",
            "Rejected",
            "Note"
        ]
    )

    notes = st.text_area("Notes")

    if st.button("Add Timeline Event", width="stretch"):
        add_timeline_event_supabase(
            candidate_id=candidate_id,
            event_date=event_date,
            event_type=event_type,
            notes=notes
        )

        st.success("Timeline event added successfully.")
        st.rerun()

    st.markdown("### Candidate Timeline")

    timeline = get_candidate_timeline_supabase(candidate_id)

    if timeline.empty:
        st.info("No timeline events found for this candidate.")
    else:
        timeline = timeline.sort_values(by="event_date", ascending=False)

        for _, event in timeline.iterrows():
            st.markdown(f"""
            <div class="card">
                <h3>{event.get("event_type", "")}</h3>
                <p><b>Date:</b> {event.get("event_date", "")}</p>
                <p>{event.get("notes", "")}</p>
            </div>
            """, unsafe_allow_html=True)

        st.dataframe(
            timeline,
            width="stretch",
            hide_index=True
        )
elif menu == "Interview Scheduler":
    st.markdown('<div class="section-title">Interview Scheduler</div>', unsafe_allow_html=True)

    tab_schedule, tab_records = st.tabs([
        "Schedule Interview",
        "Interview Records"
    ])

    with tab_schedule:
        st.subheader("Schedule new interview")

        candidates = get_candidates_supabase()

        if candidates.empty or "id" not in candidates.columns or "name" not in candidates.columns:
            st.warning("No candidates available.")
        else:
            valid_candidates = candidates.dropna(subset=["id", "name"])

            candidate_options = (
                valid_candidates["name"].astype(str)
                + " — "
                + valid_candidates["pipeline_stage"].astype(str)
                + " — ID "
                + valid_candidates["id"].astype(float).astype(int).astype(str)
            )

            selected_candidate = st.selectbox(
                "Select candidate",
                candidate_options,
                key="interview_candidate_select"
            )

            candidate_id = int(float(selected_candidate.split("ID ")[1]))

            candidate_row = valid_candidates[
                valid_candidates["id"].astype(float).astype(int) == candidate_id
            ].iloc[0]

            st.markdown("### Candidate Details")

            st.info(
                f"""
Name: {candidate_row.get('name','')}

Email: {candidate_row.get('email','')}

Country: {candidate_row.get('country','')}

Experience: {candidate_row.get('experience_years',0)} years

Skills: {candidate_row.get('skills','')}

Current Stage: {candidate_row.get('pipeline_stage','')}
"""
            )

            job_title = st.text_input("Job title")
            company = st.text_input("Company")
            interview_date = st.date_input("Interview date")
            interview_time = st.time_input("Interview time")

            interview_type = st.selectbox(
                "Interview type",
                ["Online", "Phone", "On-site", "Technical", "HR"]
            )

            notes = st.text_area("Notes")

            if st.button("Save interview", width="stretch"):
                if job_title.strip() and company.strip():
                    try:
                        result = add_interview_supabase(
                            candidate_id=candidate_id,
                            candidate_name=str(candidate_row.get("name", "")),
                            candidate_email=str(candidate_row.get("email", "")),
                            job_title=job_title,
                            company=company,
                            interview_date=interview_date,
                            interview_time=interview_time,
                            interview_type=interview_type,
                            notes=notes
                        )

                        add_timeline_event_supabase(
                            candidate_id=candidate_id,
                            event_date=interview_date,
                            event_type="Interview Scheduled",
                            notes=f"{interview_type} interview for {job_title} at {company}."
                        )

                        update_candidate_stage_supabase(
                            candidate_id,
                            "Interview Scheduled"
                        )

                        st.success("Interview scheduled successfully.")
                        st.dataframe(pd.DataFrame(result))
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error saving interview: {e}")
                else:
                    st.warning("Job title and company are required.")

    with tab_records:
        st.subheader("Scheduled interviews")

        interviews = get_interviews_supabase()

        if interviews.empty:
            st.info("No interviews scheduled yet.")
        else:
            st.dataframe(
                interviews,
                width="stretch",
                hide_index=True
            )

            if "id" in interviews.columns:
                interview_options = (
                    interviews["candidate_name"].astype(str)
                    + " - "
                    + interviews["job_title"].astype(str)
                    + " — ID "
                    + interviews["id"].astype(float).astype(int).astype(str)
                )

                selected_interview = st.selectbox(
                    "Select interview to delete",
                    interview_options
                )

                interview_id = int(float(selected_interview.split("ID ")[1]))

                confirm = st.checkbox("I confirm delete this interview")

                if st.button("Delete interview"):
                    if confirm:
                        delete_interview_supabase(interview_id)
                        st.success("Interview deleted successfully.")
                        st.rerun()
                    else:
                        st.warning("Please confirm first.")

                st.markdown("### Generate Interview Invitation Email")

                selected_email_interview = st.selectbox(
                    "Select interview for email",
                    interview_options,
                    key="interview_email_select"
                )

                email_interview_id = int(float(selected_email_interview.split("ID ")[1]))

                email_interview_row = interviews[
                    interviews["id"].astype(float).astype(int) == email_interview_id
                ].iloc[0]

                if "generated_interview_email" not in st.session_state:
                    st.session_state.generated_interview_email = ""

                if st.button("Generate invitation email", width="stretch"):
                    email_text = generate_interview_invitation_email(
                        candidate_name=str(email_interview_row.get("candidate_name", "")),
                        candidate_email=str(email_interview_row.get("candidate_email", "")),
                        job_title=str(email_interview_row.get("job_title", "")),
                        company=str(email_interview_row.get("company", "")),
                        interview_date=str(email_interview_row.get("interview_date", "")),
                        interview_time=str(email_interview_row.get("interview_time", "")),
                        interview_type=str(email_interview_row.get("interview_type", "")),
                        notes=str(email_interview_row.get("notes", ""))
                    )

                    st.session_state.generated_interview_email = email_text
                    st.success("Interview invitation email generated.")

                if st.session_state.generated_interview_email:
                    email_text = st.text_area(
                        "Generated Email",
                        st.session_state.generated_interview_email,
                        height=320
                    )

                    subject = f"Interview Invitation - {email_interview_row.get('job_title', '')}"

                    if st.button("Send email to candidate", width="stretch"):
                        success, message = send_email(
                            to_email=str(email_interview_row.get("candidate_email", "")),
                            subject=subject,
                            body=email_text
                        )

                        if success:
                            st.success(message)
                        else:
                            st.error(message)

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
    st.markdown(
        '<div class="section-title">Candidate Matching</div>',
        unsafe_allow_html=True
    )

    search_job_match = st.text_input(
        "Search job by name or title",
        placeholder="Example: Software Engineer, Python Developer, Teacher..."
    )

    search_matching_online = st.button(
        "Search online job offers for matching"
    )

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
                jobs_for_matching["job_title"].astype(str).str.lower().str.contains(
                    search_text,
                    na=False
                )
                |
                jobs_for_matching["company"].astype(str).str.lower().str.contains(
                    search_text,
                    na=False
                )
                |
                jobs_for_matching["required_skills"].astype(str).str.lower().str.contains(
                    search_text,
                    na=False
                )
            ]

    if jobs_for_matching.empty:
        st.warning(
            "No job offers found. Try another keyword or use online search."
        )

    else:

        job_options = (
            jobs_for_matching["company"].astype(str)
            + " - "
            + jobs_for_matching["job_title"].astype(str)
            + " — ID "
            + jobs_for_matching["id"].astype(float).astype(int).astype(str)
        )

        selected_job = st.selectbox(
            "Select Job Offer",
            job_options
        )

        selected_job_id = int(
            float(selected_job.split("ID ")[1])
        )

        job, matches = match_candidates(
            selected_job_id,
            candidates,
            jobs_for_matching
        )

        st.markdown(
            f"""
        <div class="card">
            <h3>{job.get('company','')} - {job.get('job_title','')}</h3>
            <p><b>Country:</b> {job.get('country','Not specified')}</p>
            <p><b>Required Skills:</b> {job.get('required_skills','Not specified')}</p>
            <p><b>Experience Required:</b> {job.get('experience_required',0)} years</p>
            <p><b>Language Required:</b> {job.get('language_required','Not specified')}</p>
            <p><b>Salary Range:</b> {job.get('salary_range','Not specified')}</p>
        </div>
        """,
            unsafe_allow_html=True
        )

        st.markdown("### Ranked Candidates")

        if matches.empty:
            st.warning("No matching candidates found.")

        else:

            st.dataframe(
                matches,
                width="stretch",
                hide_index=True
            )

            st.markdown("### Top 10 Candidates")

            top_candidates = matches.head(10)

            st.bar_chart(
                top_candidates.set_index(
                    "candidate_name"
                )["match_score"]
            )

            st.markdown("### Best Candidate")

            best_candidate = matches.iloc[0]

            st.success(
                f"""
                Best Match: {best_candidate['candidate_name']}

                Match Score: {best_candidate['match_score']}%

                Country: {best_candidate['country']}

                Experience: {best_candidate['experience_years']} years

                Matched Skills:
                {best_candidate['matched_skills']}
                """
            )
elif menu == "AI Interview Questions":

    st.markdown(
        '<div class="section-title">AI Interview Kit Generator</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Upload a resume and generate interview questions, expected answers, evaluation criteria and difficulty levels using AI."
    )

    uploaded_resume = st.file_uploader(
        "Upload candidate resume PDF",
        type=["pdf"],
        key="interview_resume_upload"
    )

    resume_text = ""

    if uploaded_resume is not None:
        resume_text = extract_text_from_pdf(uploaded_resume)
        st.success("Resume uploaded and extracted successfully.")

        with st.expander("Preview extracted resume text"):
            st.text_area(
                "Resume text",
                resume_text,
                height=220
            )

    job_title = st.text_input(
        "Job Title",
        placeholder="Python Developer"
    )

    skills = st.text_area(
        "Required Skills",
        placeholder="Python, FastAPI, Docker, AWS"
    )

    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the job description here...",
        height=180
    )

    if st.button(
        "Generate Interview Kit",
        width="stretch"
    ):

        if not resume_text.strip():
            st.warning("Please upload a resume PDF first.")
        elif not job_title.strip():
            st.warning("Please enter a job title.")
        elif not skills.strip():
            st.warning("Please enter required skills.")
        else:
            with st.spinner("Generating interview kit with Groq AI..."):

                interview_kit = generate_interview_questions(
                    resume_text=resume_text,
                    job_title=job_title,
                    skills=skills,
                    job_description=job_description
                )

            st.success("Interview kit generated successfully.")

            st.text_area(
                "Generated Interview Kit",
                interview_kit,
                height=650
            )                                           
elif menu == "Interview Scorecard":

    st.markdown(
        '<div class="section-title">Interview Scorecard</div>',
        unsafe_allow_html=True
    )

    job_title = st.text_input("Job Title")

    questions = st.text_area(
        "Interview Questions",
        height=250
    )

    answers = st.text_area(
        "Candidate Answers",
        height=350
    )

    if st.button(
        "Evaluate Candidate",
        width="stretch"
    ):
        if questions.strip() and answers.strip():

            with st.spinner("Evaluating candidate..."):

                result = evaluate_candidate(
                    job_title,
                    questions,
                    answers
                )

            st.success("Evaluation completed")

            st.markdown(result)

        else:
            st.warning(
                "Please provide questions and answers."
            )

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

        job_link = str(selected_job_row.get("job_link", ""))

        st.markdown(f"""
        <div class="card">
            <h3>{selected_job_row.get('company', '')} - {selected_job_row.get('job_title', '')}</h3>
            <p><b>Country / Location:</b> {selected_job_row.get('country', '')}</p>
            <p><b>Required skills / keyword:</b> {selected_job_row.get('required_skills', '')}</p>
            <p><b>Salary range:</b> {selected_job_row.get('salary_range', 'Not specified')}</p>
            <p><b>Job link:</b> {job_link}</p>
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
                        candidate_name=candidate_name_email,
                        job_title=str(selected_job_row.get("job_title", "")),
                        company=str(selected_job_row.get("company", "")),
                        country=str(selected_job_row.get("country", "")),
                        matched_skills=", ".join(matched_skills)
                    )

                if job_link.strip():
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

    clients = get_clients_supabase()

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

        clients = get_clients_supabase()

        st.write("Number of clients:", len(clients))

        if clients.empty:
            st.warning("No clients found in Supabase")
        else:
            st.dataframe(
                clients,
                use_container_width=True,
                hide_index=True
            )

    with tab4:
        st.subheader("Manage clients")

        clients = get_clients_supabase()

        action = st.selectbox(
            "Action",
            ["Add client", "Edit client", "Delete client"],
            key="client_action"
        )

        if action == "Add client":
            name = st.text_input("Client name", key="add_client_name")
            service = st.text_input("Service", key="add_client_service")
            deadline = st.date_input("Deadline", key="add_client_deadline")

            status = st.selectbox(
                "Status",
                ["Pending", "In Progress", "Delayed", "Completed"],
                key="add_client_status"
            )

            if st.button("Save client", key="save_client_btn"):
                    if name.strip() and service.strip():
                        try:
                            add_client_supabase(
                                name=name,
                                service=service,
                                deadline=str(deadline),
                                status=status
                            )

                            st.success("Client saved successfully. Go to Client Records to verify it.")

                        except Exception as e:
                            st.error(f"Error saving client: {e}")
                    else:
                        st.warning("Client name and service are required.")

        elif action == "Edit client":
            if clients.empty:
                st.warning("No clients available to edit.")
            else:
                client_options = (
                    clients["name"].astype(str)
                    + " - "
                    + clients["service"].astype(str)
                    + " — ID "
                    + clients["id"].astype(float).astype(int).astype(str)
                )

                selected_client_edit = st.selectbox(
                    "Select client to edit",
                    client_options,
                    key="edit_client_select"
                )

                client_id = int(float(selected_client_edit.split("ID ")[1]))

                client_row = clients[
                    clients["id"].astype(float).astype(int) == client_id
                ].iloc[0]

                edit_name = st.text_input(
                    "Client name",
                    value=str(client_row.get("name", "")),
                    key="edit_client_name"
                )

                edit_service = st.text_input(
                    "Service",
                    value=str(client_row.get("service", "")),
                    key="edit_client_service"
                )

                edit_deadline = st.date_input(
                    "Deadline",
                    key="edit_client_deadline"
                )

                status_options = ["Pending", "In Progress", "Delayed", "Completed"]

                edit_status = st.selectbox(
                    "Status",
                    status_options,
                    index=status_options.index(str(client_row.get("status", "Pending")))
                    if str(client_row.get("status", "Pending")) in status_options else 0,
                    key="edit_client_status"
                )

                if st.button("Update client", key="update_client_btn"):
                    update_client_supabase(
                        client_id,
                        edit_name,
                        edit_service,
                        str(edit_deadline),
                        edit_status
                    )

                    st.success("Client updated successfully.")
                    st.rerun()
                elif action == "Delete client":
                    if clients.empty:
                        st.warning("No clients available to delete.")
                    else:
                        client_options = (
                            clients["name"].astype(str)
                            + " - "
                            + clients["service"].astype(str)
                            + " — ID "
                            + clients["id"].astype(float).astype(int).astype(str)
                        )

                        selected_client = st.selectbox(
                            "Select client to delete",
                            client_options,
                            key="delete_client_select"
                        )

                        client_id = int(float(selected_client.split("ID ")[1]))

                        confirm = st.checkbox(
                            "I confirm delete",
                            key="confirm_delete_client"
                        )

                        if st.button("Delete client", key="delete_client_btn"):
                            if confirm:
                                delete_client_supabase(client_id)
                                st.success("Client deleted successfully.")
                            else:
                                st.warning("Please confirm first.")

        elif action == "Delete client":
            if clients.empty:
                st.warning("No clients available to delete.")
            else:
                client_options = (
                    clients["name"].astype(str)
                    + " - "
                    + clients["service"].astype(str)
                    + " — ID "
                    + clients["id"].astype(float).astype(int).astype(str)
                )

                selected_client = st.selectbox(
                    "Select client to delete",
                    client_options,
                    key="delete_client_select"
                )

                client_id = int(float(selected_client.split("ID ")[1]))

                confirm = st.checkbox(
                    "I confirm delete",
                    key="confirm_delete_client"
                )

                if st.button("Delete client", key="delete_client_btn"):
                    if confirm:
                        delete_client_supabase(client_id)
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


elif st.session_state.page == "Settings":
    st.markdown('<div class="section-title">Settings</div>', unsafe_allow_html=True)

    st.markdown("### Account")

    current_user = st.session_state.get("username", "admin")
    role = st.session_state.get("role", "Admin")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Username", current_user)

    with col2:
        st.metric("Role", role)

    st.markdown("### Change Password")

    st.info("Password changes are saved automatically in Supabase.")

    old_password = st.text_input("Current password", type="password")
    new_password = st.text_input("New password", type="password")
    confirm_password = st.text_input("Confirm new password", type="password")

    if st.button("Change password", use_container_width=True, key="settings_change_password_btn"):
        user = get_user(current_user, old_password)

        if not user:
            st.error("Current password is incorrect.")

        elif new_password != confirm_password:
            st.error("New passwords do not match.")

        elif len(new_password) < 8:
            st.warning("Password must contain at least 8 characters.")

        else:
            update_password(current_user, new_password)

            st.success("Password changed successfully. Please log in again.")

            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.role = None
            st.session_state.page = "Dashboard"
            st.rerun()

    st.divider()

    st.subheader("User Management")

    if st.session_state.get("role") != "Admin":
        st.warning("Only Admin users can manage accounts.")

    else:
        users = get_all_users()

        if users:
            st.dataframe(users, use_container_width=True, hide_index=True)
        else:
            st.info("No users found.")

        user_tab1, user_tab2, user_tab3 = st.tabs([
            "Add User",
            "Edit User",
            "Delete User"
        ])

        with user_tab1:
            st.markdown("#### Add user")

            new_username = st.text_input("Username", key="add_user_username")
            new_password = st.text_input("Password", type="password", key="add_user_password")
            new_role = st.selectbox(
                "Role",
                ["Admin", "Recruiter", "Manager"],
                key="add_user_role"
            )
            new_active = st.checkbox("Active", value=True, key="add_user_active")

            if st.button("Create User", use_container_width=True, key="create_user_btn"):
                if not new_username.strip():
                    st.warning("Please enter a username.")

                elif not new_password.strip():
                    st.warning("Please enter a password.")

                elif len(new_password) < 8:
                    st.warning("Password must contain at least 8 characters.")

                elif username_exists(new_username):
                    st.warning("An account with this username already exists.")
                    st.info("Tip: Use the employee's email or company username.")

                else:
                    try:
                        create_user(
                            new_username,
                            new_password,
                            new_role,
                            new_active
                        )

                        st.success(f"User '{new_username}' created successfully.")
                        st.rerun()

                    except Exception:
                        st.error("Unable to create user. Please try again.")

        with user_tab2:
            st.markdown("#### Edit user")

            if not users:
                st.info("No users available.")
            else:
                user_options = [
                    f"{u['username']} — {u['role']} — ID {u['id']}"
                    for u in users
                ]

                selected_user = st.selectbox(
                    "Select user",
                    user_options,
                    key="edit_user_select"
                )

                selected_id = int(selected_user.split("ID ")[1])

                selected_row = next(
                    u for u in users if int(u["id"]) == selected_id
                )

                edit_username = st.text_input(
                    "Username",
                    value=selected_row["username"],
                    key=f"edit_username_{selected_id}"
                )

                role_options = ["Admin", "Recruiter", "Manager"]

                edit_role = st.selectbox(
                    "Role",
                    role_options,
                    index=role_options.index(selected_row["role"])
                    if selected_row["role"] in role_options else 1,
                    key=f"edit_role_{selected_id}"
                )

                edit_active = st.checkbox(
                    "Active",
                    value=bool(selected_row["is_active"]),
                    key=f"edit_active_{selected_id}"
                )

                if st.button(
                    "Update User",
                    use_container_width=True,
                    key=f"update_user_{selected_id}"
                ):
                    if not edit_username.strip():
                        st.warning("Username is required.")

                    elif username_exists(edit_username, exclude_user_id=selected_id):
                        st.error("This username already exists.")

                    else:
                        try:
                            update_user(
                                selected_id,
                                edit_username,
                                edit_role,
                                edit_active
                            )

                            st.success("User updated successfully in Supabase.")
                            st.rerun()

                        except Exception:
                            st.error("Unable to update user. Please try again.")

        with user_tab3:
            st.markdown("#### Delete user")

            if not users:
                st.info("No users available.")
            else:
                user_options_delete = [
                    f"{u['username']} — ID {u['id']}"
                    for u in users
                ]

                selected_delete_user = st.selectbox(
                    "Select user to delete",
                    user_options_delete,
                    key="delete_user_select"
                )

                delete_id = int(selected_delete_user.split("ID ")[1])
                delete_username = selected_delete_user.split(" — ID ")[0]

                confirm_delete = st.checkbox(
                    "I confirm deleting this user",
                    key=f"confirm_delete_{delete_id}"
                )

                if st.button(
                    "Delete User",
                    use_container_width=True,
                    key=f"delete_user_{delete_id}"
                ):
                    if not confirm_delete:
                        st.warning("Please confirm first.")

                    elif st.session_state.get("username") == delete_username:
                        st.error("You cannot delete your own account.")

                    else:
                        try:
                            delete_user(delete_id)

                            st.success("User deleted successfully from Supabase.")
                            st.rerun()

                        except Exception:
                            st.error("Unable to delete user. Please try again.")

    st.divider()

    st.subheader("System")

    sys_col1, sys_col2, sys_col3 = st.columns(3)

    with sys_col1:
        st.metric("Version", "1.0.0")

    with sys_col2:
        st.metric("Authentication", "Supabase ")

    with sys_col3:
        st.metric("Environment", "Local")