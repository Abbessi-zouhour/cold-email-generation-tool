# TalentBridge — AI-Powered Recruitment Intelligence Platform

TalentBridge is an AI-powered recruitment intelligence platform designed to help recruiters, HR teams, agencies and career consultants manage candidates, analyze resumes, match profiles with job offers, calculate ATS scores and generate personalized recruitment communication.

## Features

* Dynamic candidate management with SQLite
* Add, edit and delete candidates
* Candidate pipeline with recruitment stages
* Candidate matching based on job requirements
* Online job search using Adzuna, JSearch and Remotive APIs
* ATS score calculator using uploaded resumes and job offers
* Resume PDF parsing
* Job offer analyzer with candidate suggestions from the database
* Personalized email generator
* Cover letter generator
* Client communication agent
* Dynamic dashboard with recruitment KPIs
* AI assistant for recruitment insights

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python
* Pandas
* SQLite

### AI & LLM

* LangChain
* Groq API
* Llama 3.3 70B Versatile

### Document Processing

* PDFPlumber

### Job APIs

* Adzuna API
* JSearch API via RapidAPI
* Remotive API

## Project Structure

```text
TalentBridge/
│
├── app.py
├── database_manager.py
├── requirements.txt
├── README.md
├── .env
│
├── assets/
│   ├── main.css
│   └── images/
│
├── database/
│   ├── talentbridge.db
│   ├── candidates.csv
│   ├── jobs.csv
│   └── clients.csv
│
├── services/
│   ├── assistant_agent.py
│   ├── ats_score.py
│   ├── candidate_matcher.py
│   ├── client_agent.py
│   ├── cover_letter_generator.py
│   ├── cv_parser.py
│   ├── email_generator.py
│   ├── job_analyzer.py
│   ├── job_api.py
│   └── resume_reader.py
```

## Environment Variables

Create a `.env` file in the project root:

```env
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
RAPIDAPI_KEY=your_rapidapi_key
GROQ_API_KEY=your_groq_api_key
```

Do not push `.env` to GitHub.

## Installation

```bash
git clone https://github.com/Abbessi-zouhour/cold-email-generation-tool.git
cd cold-email-generation-tool
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Database

The application uses SQLite through:

```text
database/talentbridge.db
```

The database stores:

* Candidates
* Jobs
* Clients

The CSV files are used as seed data and backup references.

## Main Modules

### Dashboard

Displays live recruitment KPIs, candidate status, pipeline stages, latest candidates and latest job opportunities.

### Candidates

Allows recruiters to add, edit, delete and view candidates from SQLite.

### Candidate Pipeline

Displays candidates by recruitment stage:

* Applied
* Screening
* Interview Scheduled
* Client Review
* Offer Sent
* Hired
* Rejected

### Job Offers

Searches job offers from multiple online APIs and displays direct application links.

### Candidate Matching

Matches candidates from SQLite with selected job offers.

### ATS Score

Compares uploaded resumes against selected job offers and calculates compatibility.

### Email Generator

Generates personalized recruitment emails based on uploaded resumes and online job offers.

### Job Analyzer

Analyzes job descriptions and suggests matching candidates from the SQLite database.

### Client Communication Agent

Generates delay messages and progress updates for clients stored in SQLite.

## Future Improvements

* Drag-and-drop candidate pipeline
* Candidate profile pages
* Email sending integration
* Interview scheduler
* Advanced AI matching with embeddings
* Recruiter analytics dashboard
* Authentication and user roles

## Author

Built by Zouhour Abbessi as an AI recruitment SaaS project.
