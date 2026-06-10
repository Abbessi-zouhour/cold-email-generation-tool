# TalentBridge

## AI-Powered Recruitment Intelligence Platform

TalentBridge is a modern recruitment intelligence platform that combines traditional recruitment workflows with Generative AI to help recruiters, agencies, and career service providers manage candidates, evaluate resumes, communicate with clients, and accelerate hiring decisions.

The platform integrates AI-powered candidate matching, CV parsing, ATS scoring, cover letter generation, job analysis, and client communication into a single recruitment workspace.

---

## Key Features

### Candidate Management

Manage and track candidate profiles including:

* Personal information
* Technical skills
* Languages
* Experience level
* Recruitment status

### Job Management

Store and manage international job opportunities:

* Company
* Country
* Job title
* Required skills
* Experience requirements
* Salary ranges
* Language requirements

### Candidate Matching Engine

Automatically rank candidates against job opportunities using:

* Skill matching
* Experience validation
* Match scoring

Recruiters can instantly identify the most relevant profiles for a specific role.

### Candidate Recruitment Pipeline

Track candidates through the hiring process:

* Applied
* Screening
* Interview Scheduled
* Client Review
* Offer Sent
* Hired
* Rejected

### AI CV Parser

Upload a resume in PDF format and automatically extract:

* Name
* Email
* Phone
* Country
* Skills
* Languages
* Experience

### ATS Score Calculator

Evaluate how well a resume matches a target job description.

The system provides:

* ATS score percentage
* Matched skills
* Missing skills
* Resume improvement recommendations

### AI Email Generator

Generate personalized recruitment emails based on:

* Candidate profile
* Job opportunity
* Company information
* Matching skills

### AI Cover Letter Generator

Generate customized cover letters for candidates based on:

* Job requirements
* Candidate skills
* Experience level

### AI Job Analyzer

Convert unstructured job descriptions into structured information:

* Job title
* Required skills
* Experience requirements
* Language requirements
* Salary information

### Client Communication Agent

Generate professional client communications including:

* Delay notifications
* Progress updates
* Service delivery updates
* Resume writing project updates
* Cover letter project updates

---

## System Architecture

```text
┌──────────────────────────────┐
│      Streamlit Frontend      │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│            app.py            │
│      Main Application UI     │
└───────────────┬──────────────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼

 Matching    AI Services   Client
 Engine                   Communication

                │
                ▼

┌──────────────────────────────┐
│      Groq Llama 3.3 70B      │
│      (LangChain + Groq)      │
└──────────────────────────────┘

                │
                ▼

┌──────────────────────────────┐
│         CSV Databases        │
│ Jobs • Candidates • Clients  │
└──────────────────────────────┘
```

---

## Project Structure

```text
TalentBridge/
│
├── app.py
│
├── database/
│   ├── candidates.csv
│   ├── jobs.csv
│   └── clients.csv
│
├── models/
│   └── llm.py
│
├── services/
│   ├── ats_score.py
│   ├── candidate_matcher.py
│   ├── client_agent.py
│   ├── cover_letter_generator.py
│   ├── cv_parser.py
│   ├── email_generator.py
│   ├── job_analyzer.py
│   └── resume_reader.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### Data Processing

* Pandas

### AI & LLM

* LangChain
* Groq API
* Llama 3.3 70B Versatile

### PDF Processing

* pdfplumber

### Data Storage

* CSV Databases

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/cold-email_generation-tool.git

cd cold-email_generation-tool
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## Running the Application

```bash
streamlit run app.py
```

or

```bash
python -m streamlit run app.py
```

Application URL:

```text
http://localhost:8501
```

---

## Example Workflow

### Recruitment Workflow

1. Create or review job opportunities.
2. Match candidates automatically.
3. Review ATS scores.
4. Analyze candidate resumes.
5. Generate personalized outreach emails.
6. Move candidates through the recruitment pipeline.
7. Send opportunities to selected candidates.

### Career Services Workflow

1. Upload a client resume.
2. Analyze ATS compatibility.
3. Generate a cover letter.
4. Track project progress.
5. Generate client updates and delay notifications.

---

## Future Roadmap

### Recruitment Intelligence

* AI Recruitment Copilot
* Semantic Candidate Search
* Interview Scheduling Agent
* Candidate Recommendation Agent
* Automated Job Scraping

### Platform Features

* User Authentication
* Recruiter Accounts
* Admin Dashboard
* PostgreSQL Database
* Cloud Deployment

### AI Enhancements

* Multi-Agent Architecture
* Retrieval-Augmented Generation (RAG)
* Candidate Knowledge Base
* Automated Talent Insights

---

## Screenshots

Create a folder:

```text
screenshots/
```

Add screenshots such as:

```text
dashboard.png
candidate-matching.png
ats-score.png
cv-parser.png
client-agent.png
```

Then embed them:

```markdown
![Dashboard](screenshots/dashboard.png)
![ATS Score](screenshots/ats-score.png)
```

---

## Author

TalentBridge was developed as an AI-powered recruitment and career services platform demonstrating how Generative AI can enhance recruitment workflows, candidate evaluation, and client communication.

---

## License

This project is intended for educational, research, and portfolio purposes.
