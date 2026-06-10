# TalentBridge

## AI-Powered Recruitment Intelligence Platform

TalentBridge is a modern AI-powered recruitment intelligence platform that helps recruiters, agencies, HR teams, and career consultants streamline hiring workflows through automation, data analysis, and Generative AI.

The platform combines recruitment management, candidate evaluation, job discovery, ATS optimization, and AI-powered communication into a single SaaS-style application.

---

# Features

## Recruitment Dashboard

Monitor recruitment activity through a centralized dashboard:

* Candidate statistics
* Recruitment pipeline overview
* Open opportunities
* Hiring insights
* Talent availability

---

## Candidate Management

Manage candidate profiles including:

* Personal information
* Contact details
* Technical skills
* Languages
* Experience level
* Recruitment status

Users can upload their own candidate datasets.

---

## Online Job Search

TalentBridge can automatically retrieve jobs from online job sources.

Recruiters can:

* Search jobs by keyword
* Discover remote opportunities
* Match candidates against live jobs

Example searches:

* Python Developer
* Data Analyst
* DevOps Engineer
* Machine Learning Engineer
* React Developer

---

## Job Management

Manage and review opportunities including:

* Company
* Country
* Job title
* Required skills
* Experience requirements
* Language requirements
* Salary information

---

## Candidate Matching Engine

Automatically rank candidates against job opportunities using:

* Skill matching
* Experience validation
* Match scoring

Recruiters can instantly identify the best profiles for any position.

---

## Recruitment Pipeline

Track candidates across stages:

* Applied
* Screening
* Interview Scheduled
* Client Review
* Offer Sent
* Hired
* Rejected

---

## ATS Score Calculator

Upload a resume PDF and compare it against a target role.

Outputs include:

* ATS compatibility score
* Matched skills
* Missing skills
* Resume recommendations

---

## AI CV Parser

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

## AI Job Analyzer

Convert unstructured job descriptions into structured information:

* Job title
* Required skills
* Required experience
* Salary information
* Language requirements

---

## AI Recruitment Email Generator

Generate personalized outreach emails using:

* Candidate profile
* Job opportunity
* Company information
* Matching skills

---

## AI Cover Letter Generator

Generate customized cover letters from:

* Uploaded resume PDF
* Job description

The system automatically tailors the cover letter to the role and highlights relevant experience.

---

## Client Communication Agent

Generate professional client communications including:

* Delay notifications
* Progress updates
* Delivery updates
* Service communications

---

## AI Assistant Chatbot

TalentBridge includes an AI-powered recruitment assistant capable of answering questions about candidates, jobs, resumes, ATS scores, and recruitment workflows.

The assistant can:

* Analyze uploaded datasets
* Explain ATS scores
* Recommend candidates
* Summarize jobs
* Answer recruitment questions
* Provide hiring insights
* Assist recruiters with decision-making

Example questions:

* Which candidate is the best fit for this role?
* Explain this ATS score.
* What skills are missing from this resume?
* Recommend candidates for a Python position.
* Summarize available opportunities.

Powered by:

* Groq API
* LangChain
* Llama 3.3 70B Versatile

---

# User Data Upload

TalentBridge supports custom datasets.

Users can upload:

## Candidates CSV

Required format:

```csv
id,name,email,phone,country,experience_years,languages,skills,status,pipeline_stage
```

## Clients CSV

Required format:

```csv
id,name,email,service,deadline,status,notes
```

If no dataset is uploaded, TalentBridge automatically loads demo data.

---

# Technology Stack

## Frontend

* Streamlit

## Backend

* Python

## Data Processing

* Pandas

## PDF Processing

* pdfplumber

## HTTP & APIs

* Requests

## AI & LLM

* Groq API
* LangChain
* LangChain-Groq
* Llama 3.3 70B Versatile

## Job Discovery

* Remotive API

---

# Project Structure

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
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installation

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

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

# Run Locally

```bash
streamlit run app.py
```

---

# Deployment

TalentBridge is designed for deployment on Streamlit Community Cloud.

Required Streamlit Secret:

```toml
GROQ_API_KEY="your_groq_api_key"
```

---

# Future Roadmap

## Recruitment Intelligence

* Semantic candidate search
* Candidate recommendation engine
* Resume ranking system
* Interview scheduling assistant

## Platform Features

* User authentication
* Recruiter accounts
* PostgreSQL integration
* Multi-user workspace
* Role-based access control

## AI Enhancements

* Multi-agent recruitment copilot
* RAG-powered candidate search
* Talent knowledge base
* Automated hiring insights

---

# Author

Developed by Zouhour Abbessi.

TalentBridge demonstrates how Generative AI can enhance recruitment workflows, candidate evaluation, hiring decisions, and client communication.

---

# License

Educational, portfolio, and research purposes.
