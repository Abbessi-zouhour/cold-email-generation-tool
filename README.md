# TalentBridge – AI-Powered Recruitment Intelligence Platform

## Overview

TalentBridge is an AI-powered recruitment platform designed to help recruitment agencies and talent acquisition teams identify the best candidates for international job opportunities.

The platform combines traditional recruitment workflows with Large Language Models (LLMs) to automate candidate evaluation, job analysis, CV parsing, and personalized outreach.

Built with Streamlit, LangChain, and Groq's Llama models, TalentBridge provides recruiters with a centralized workspace for managing candidates and accelerating hiring decisions.

---

## Features

### Candidate Management

* View and manage candidate profiles
* Track candidate availability and recruitment status
* Store skills, experience, languages, and contact information

### Job Management

* Browse and manage international job opportunities
* View required skills, experience, language requirements, and salary ranges

### AI Candidate Matching

* Automatically match candidates to job offers
* Skill-based scoring system
* Experience-based ranking
* Candidate recommendation engine

### AI Email Generation

Generate personalized recruitment emails tailored to:

* Candidate profile
* Job opportunity
* Matching skills
* Company information

### AI Job Offer Analyzer

Extract structured information from unstructured job descriptions:

* Job title
* Country
* Required skills
* Required experience
* Language requirements
* Salary information

### AI CV Parser

Convert raw CV text into structured candidate profiles:

* Name
* Email
* Phone
* Country
* Skills
* Experience
* Languages

---

## System Architecture

```text
┌─────────────────────────┐
│      Streamlit UI       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│      Application        │
│        app.py           │
└────────────┬────────────┘
             │
 ┌───────────┼───────────┐
 ▼           ▼           ▼
Matching   Email      Analysis
Engine   Generator    Services
             │
             ▼
      Groq Llama 3.3
         70B Model
             │
             ▼
       Recruitment AI
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
│   └── jobs.csv
│
├── models/
│   └── llm.py
│
├── services/
│   ├── candidate_matcher.py
│   ├── email_generator.py
│   ├── job_analyzer.py
│   └── cv_parser.py
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

### Environment Management

* Python Dotenv

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

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

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
GROQ_API_KEY=your_groq_api_key
```

---

## Running the Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## Example Workflow

1. Recruiter selects a job offer.
2. The matching engine ranks candidates.
3. The recruiter reviews top matches.
4. AI generates personalized outreach emails.
5. New CVs can be parsed automatically.
6. Job descriptions can be analyzed and structured using AI.

---

## Future Improvements

* Resume upload (PDF/DOCX)
* Semantic candidate matching using embeddings
* ATS integration
* Candidate recommendation engine
* Automated interview scheduling
* Multi-language recruitment support
* Recruiter analytics dashboard
* PostgreSQL database integration
* Cloud deployment

---

## Author

Developed as an AI Recruitment Intelligence Platform project focused on combining recruitment workflows with Generative AI technologies.

---

## License

This project is intended for educational and portfolio purposes.
