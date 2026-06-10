# TalentBridge

## AI-Powered Recruitment Intelligence Platform

TalentBridge is an AI-powered recruitment intelligence platform that helps recruiters, agencies, and career service providers manage candidates, discover job opportunities, analyze resumes, generate professional communications, and automate recruitment workflows.

The platform combines recruitment operations with Generative AI to improve hiring efficiency and candidate evaluation.

---

## Features

### Recruitment Dashboard

Monitor recruitment activity through an intuitive dashboard:

* Total candidates
* Open opportunities
* Candidate availability
* Recruitment pipeline overview
* Hiring statistics

---

### Candidate Management

Manage candidate profiles including:

* Personal information
* Technical skills
* Languages
* Experience level
* Recruitment status

Users can upload their own candidate datasets via CSV.

---

### Online Job Search

TalentBridge can automatically fetch jobs from online job sources.

Recruiters can:

* Search jobs by keyword
* Retrieve real job opportunities
* Match candidates against live opportunities

Examples:

* Python Developer
* Data Analyst
* Machine Learning Engineer
* DevOps Engineer
* Frontend Developer

---

### Job Management

Display and analyze:

* Company
* Country
* Job title
* Required skills
* Experience requirements
* Salary information
* Language requirements

---

### Candidate Matching Engine

Automatically rank candidates against job opportunities using:

* Skill matching
* Experience validation
* Match scoring

Recruiters can instantly identify the most relevant profiles.

---

### Recruitment Pipeline

Track candidates through:

* Applied
* Screening
* Interview Scheduled
* Client Review
* Offer Sent
* Hired
* Rejected

---

### ATS Score Calculator

Upload a resume PDF and compare it against a target role.

Outputs:

* ATS compatibility score
* Matched skills
* Missing skills
* Resume improvement recommendations

---

### AI CV Parser

Upload a PDF resume and automatically extract:

* Name
* Email
* Phone
* Country
* Skills
* Languages
* Experience

Powered by Groq LLM.

---

### AI Job Analyzer

Convert unstructured job descriptions into structured information:

* Job title
* Required skills
* Required experience
* Salary information
* Language requirements

---

### AI Recruitment Email Generator

Generate personalized outreach emails based on:

* Candidate profile
* Job opportunity
* Company information
* Candidate skills

---

### AI Cover Letter Generator

Generate customized cover letters using:

* Uploaded PDF resume
* Job description

The AI automatically tailors the cover letter to the position and highlights relevant experience.

---

### Client Communication Agent

Generate professional client communications including:

* Delay notifications
* Progress updates
* Service delivery updates

---

## User Data Upload

Users can upload:

### Candidates Dataset

CSV format containing:

```text
id,name,email,phone,country,experience_years,languages,skills,status,pipeline_stage
```

### Clients Dataset

CSV format containing:

```text
id,name,email,service,deadline,status,notes
```

If no datasets are uploaded, TalentBridge uses default demo datasets.

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### Data Processing

* Pandas

### PDF Processing

* pdfplumber

### AI & LLM

* Groq API
* Llama 3.3 70B Versatile
* LangChain
* LangChain-Groq

### Job Discovery

* Remotive API

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
│   ├── job_api.py
│   └── resume_reader.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Abbessi-zouhour/cold-email-generation-tool.git
cd cold-email-generation-tool
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Run Locally

```bash
streamlit run app.py
```

---

## Deployment

TalentBridge is designed to be deployed on Streamlit Community Cloud.

Required Streamlit Secret:

```toml
GROQ_API_KEY="your_groq_api_key"
```

---

## Future Roadmap

### Recruitment Intelligence

* Semantic candidate search
* AI recruitment copilot
* Candidate recommendation engine
* Interview scheduling assistant

### Platform Features

* User authentication
* Recruiter accounts
* PostgreSQL database
* Multi-user workspaces

### AI Enhancements

* Multi-agent architecture
* RAG-powered candidate search
* Talent knowledge base
* Automated hiring insights

---

## Author

Developed by Zouhour Abbessi as an AI-powered recruitment intelligence platform demonstrating how Generative AI can enhance recruitment workflows, candidate evaluation, and client communication.

---

## License

Educational, portfolio, and research purposes.
