# TalentBridge

## AI-Powered Recruitment Intelligence Platform

TalentBridge is a modern AI-powered recruitment intelligence platform designed for recruiters, staffing agencies, HR teams, and career consultants.

The platform combines recruitment management, candidate sourcing, ATS optimization, AI-powered candidate evaluation, interview management, and recruitment analytics into a single SaaS-style application.

---

# Features

## Recruitment Dashboard

Real-time recruitment analytics dashboard with:

* Total candidates
* Total jobs
* Total clients
* Scheduled interviews
* Hiring rate
* Open positions
* Available candidates
* Pipeline distribution
* Candidate country distribution
* Job market analytics

---

## Candidate Management

Manage candidate profiles stored in SQLite.

Features:

* Personal information
* Contact details
* Skills
* Languages
* Experience
* Candidate status
* Pipeline stage

---

## Candidate Matching Engine

Automatically match candidates against jobs using:

* Skills matching
* Experience matching
* Country matching
* Match scoring

Outputs:

* Match percentage
* Best candidates ranking
* Recommended candidates

---

## Candidate Pipeline

Dynamic ATS pipeline management.

Stages:

* Applied
* Screening
* Interview Scheduled
* Client Review
* Offer Sent
* Hired
* Rejected

Features:

* Move candidates between stages
* Real-time pipeline updates
* SQLite persistence

---

## Candidate Timeline

Track candidate history and recruitment events.

Examples:

* Application received
* Screening completed
* Interview completed
* Client review
* Offer sent
* Hired

Features:

* Add timeline events
* View full candidate history
* Delete timeline events

---

## Online Job Search

Search live job opportunities from multiple job sources.

Current integrations:

* Adzuna API
* Remotive API
* RapidAPI integrations (optional)

Search by:

* Job title
* Skills
* Keywords
* Country

Supported countries include:

* United Kingdom
* France
* Canada
* USA
* Germany
* Belgium
* Netherlands
* Australia
* Italy
* Spain
* India
* Singapore
* South Africa

---

## Job Analyzer

Convert unstructured job descriptions into structured recruitment data.

Extracts:

* Job title
* Required skills
* Experience requirements
* Language requirements
* Salary information

Includes candidate recommendations from the database.

---

## ATS Resume Score Calculator

Compare resumes against job opportunities.

Outputs:

* ATS score
* Matching skills
* Missing skills
* Improvement suggestions

---

## AI Resume Parser

Upload a resume PDF and automatically extract:

* Name
* Email
* Phone
* Country
* Skills
* Languages
* Experience

Powered by Groq LLM.

---

## AI Email Generator

Generate personalized application emails using:

* Resume content
* Job information
* Candidate profile
* Required skills

Includes:

* Online job selection
* Resume upload
* Job link insertion

---

## AI Cover Letter Generator

Generate customized cover letters using:

* Uploaded resume
* Job description

AI automatically adapts content to the target role.

---

## Interview Scheduler

Manage candidate interviews.

Features:

* Schedule interviews
* Interview records
* Candidate association
* SQLite storage

Interview types:

* Online
* Phone
* On-site
* Technical
* HR

---

## Interview Invitation Email Generator

Generate professional interview invitation emails using AI.

Includes:

* Candidate information
* Job details
* Interview details
* Professional formatting

---

## AI Interview Questions Generator

Generate dynamic interview questions based on:

* Uploaded resume
* Job title
* Required skills
* Job description

Outputs:

* Technical questions
* HR questions
* Behavioral questions
* Case studies
* Evaluation criteria

---

## AI Interview Scorecard

Evaluate candidate interview answers using AI.

Outputs:

* Technical score
* Communication score
* Problem solving score
* Overall score
* Hiring recommendation

Recommendations:

* Strong Hire
* Hire
* Maybe
* Reject

---

## Client Communication Agent

Generate professional client communications.

Includes:

* Delay notifications
* Progress updates
* Service updates
* Delivery communications

Client records are stored dynamically in SQLite.

---

## AI Assistant

AI-powered recruitment assistant.

Capabilities:

* Candidate analysis
* Job analysis
* ATS explanations
* Recruitment insights
* Hiring recommendations
* Database exploration

Powered by:

* Groq API
* LangChain
* Llama 3.3 70B Versatile

---

# Technology Stack

## Frontend

* Streamlit

## Backend

* Python

## Database

* SQLite

## Data Processing

* Pandas

## PDF Processing

* pdfplumber

## APIs

* Adzuna API
* Remotive API
* RapidAPI

## AI & LLM

* Groq API
* LangChain
* LangChain-Groq
* Llama 3.3 70B Versatile

---

# Project Structure

```text
TalentBridge/
│
├── app.py
│
├── database/
│
├── models/
│   └── llm.py
│
├── services/
│   ├── analytics_dashboard.py
│   ├── assistant_agent.py
│   ├── ats_score.py
│   ├── candidate_timeline.py
│   ├── candidate_matcher.py
│   ├── client_agent.py
│   ├── cover_letter_generator.py
│   ├── cv_parser.py
│   ├── email_generator.py
│   ├── email_sender.py
│   ├── interview_email.py
│   ├── interview_questions.py
│   ├── interview_scheduler.py
│   ├── interview_scorecard.py
│   ├── job_analyzer.py
│   ├── job_api.py
│   ├── pipeline_manager.py
│   ├── recommendation_engine.py
│   └── resume_reader.py
│
├── assets/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key

ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key

RAPIDAPI_KEY=your_rapidapi_key

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

---

# Installation

```bash
git clone https://github.com/your-username/TalentBridge.git

cd TalentBridge

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

---

# Run Locally

```bash
streamlit run app.py
```

---

# Roadmap

Future improvements:

* User authentication
* PostgreSQL cloud database
* Multi-user workspaces
* Real drag-and-drop pipeline
* Recruiter KPI dashboard
* Email tracking
* AI interview copilot
* Candidate semantic search
* Resume ranking engine

---

# Author

Developed by Zouhour Abbessi.

TalentBridge demonstrates how Artificial Intelligence can transform recruitment workflows, candidate evaluation, hiring decisions, interview management, and talent acquisition processes.

---

# License

Educational, portfolio, and research purposes.
