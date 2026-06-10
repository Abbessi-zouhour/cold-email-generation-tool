# TalentBridge

## AI-Powered Recruitment Intelligence Platform

TalentBridge is an AI-powered recruitment intelligence platform designed to help recruiters, agencies, and career service providers manage candidates, evaluate resumes, match talent to jobs, and automate professional communication.

The platform combines recruitment workflows with Generative AI to accelerate hiring decisions and improve candidate evaluation.

---

## Live Demo

Deployable on Streamlit Cloud.

---

## Features

### Recruitment Dashboard

Monitor recruitment activity through a centralized dashboard including:

* Total candidates
* Open positions
* Available talent
* Placed candidates
* Recruitment pipeline overview

---

### Candidate Management

Manage candidate profiles including:

* Personal information
* Skills
* Languages
* Experience level
* Recruitment status

---

### Job Management

Store and manage international job opportunities:

* Company
* Country
* Job title
* Required skills
* Experience requirements
* Salary range
* Language requirements

---

### Candidate Matching Engine

Automatically rank candidates against job opportunities using:

* Skill matching
* Experience validation
* Match scoring

The platform identifies the most relevant candidates for a selected role.

---

### ATS Score Calculator

Upload a resume PDF and compare it against a target job opportunity.

Outputs include:

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
* Language requirements
* Salary information

---

### AI Recruitment Email Generator

Generate personalized recruitment emails based on:

* Candidate profile
* Job opportunity
* Matching skills
* Company information

---

### AI Cover Letter Generator

Generate customized cover letters using:

* Uploaded PDF resume
* Job description

The AI automatically tailors the cover letter to the position while highlighting relevant experience and skills.

---

### Client Communication Agent

Generate professional client communications including:

* Delay notifications
* Progress updates
* Service delivery messages

---

### Candidate Pipeline

Track candidates through recruitment stages:

* Applied
* Screening
* Interview Scheduled
* Client Review
* Offer Sent
* Hired
* Rejected

---

## User Dataset Upload

TalentBridge supports custom datasets.

Users can upload:

* Candidates CSV
* Jobs CSV
* Clients CSV

If no files are uploaded, the application automatically uses demo datasets.

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
├── requirements.txt
└── README.md
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

## Future Improvements

* User authentication
* PostgreSQL database
* Semantic candidate search
* AI recruitment copilot
* Interview scheduling assistant
* Resume ranking system
* Recruiter dashboard
* Multi-user workspace

---

## Author

Developed by Zouhour Abbessi as an AI-powered recruitment intelligence platform demonstrating the integration of Generative AI into recruitment and career services workflows.

---

## License

This project is intended for educational, portfolio, and research purposes.
