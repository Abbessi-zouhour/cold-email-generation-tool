# TalentBridge 🚀

## AI-Powered Recruitment Intelligence Platform

TalentBridge is a modern AI-powered recruitment platform built with **Streamlit**, **Supabase**, and **OpenAI**. It helps recruiters manage candidates, jobs, interviews, CRM activities, candidate rankings, reports, and recruitment workflows from a single dashboard.

---

## 🌟 Features

### 🔐 Authentication & User Management

- Secure Login System
- Multi-User Authentication
- Role-Based Access Control (RBAC)
  - Admin
  - Recruiter
  - Manager
- User Creation
- User Editing
- User Deletion
- Password Management
- Session Management

---

### 👥 Candidate Management

- Candidate Database
- Candidate Search & Filtering
- Candidate Profiles
- Candidate Status Tracking
- Candidate Pipeline
- Candidate Timeline
- Candidate Notes & Comments

---

### 📋 Job Management

- Job Offers Management
- Online Job Search Integration
- Job Analysis
- Candidate Matching
- ATS Evaluation

---

### 🤖 AI Recruitment Features

#### AI Assistant

Recruitment-focused assistant capable of answering questions about:

- Candidates
- Jobs
- ATS Scores
- Recruitment Workflows
- Hiring Decisions

#### AI Candidate Ranking

Automatically ranks candidates against job requirements based on:

- Skills
- Experience
- ATS Compatibility
- AI Matching Score

---

### 📄 Resume Processing

- CV Parser
- Resume Analysis
- ATS Score Generator
- Skills Extraction
- Candidate Data Extraction

---

### 📧 Communication Tools

#### Email Generator

Generate professional:

- Outreach Emails
- Interview Invitations
- Follow-Up Emails
- Rejection Emails
- Offer Letters

#### Client Communication Agent

Generate client-facing communications and recruitment updates.

---

### 📅 Interview Management

- Interview Scheduler
- Interview Reminder Emails
- Interview Scorecards
- AI Interview Questions Generator

---

### 🏢 Recruitment CRM

Manage:

- Companies
- Clients
- Contacts
- Industries
- Recruitment Relationships

---

### 📊 Reporting & Analytics

- Dashboard Analytics
- Candidate Metrics
- Job Metrics
- Hiring Metrics
- Pipeline Analytics
- PDF Export Reports

---

### 📝 Activity Logs

Track all important platform actions:

- User Creation
- User Updates
- User Deletion
- CRM Actions
- Candidate Actions
- AI Actions
- System Events

---

## 🛠️ Tech Stack

### Frontend

- Streamlit
- HTML
- CSS

### Backend

- Python

### Database

- Supabase
- PostgreSQL

### Artificial Intelligence

- OpenAI API

### Email

- Gmail SMTP

### Deployment

- Streamlit Community Cloud

### Version Control

- Git
- GitHub

---

## 📂 Project Structure

```text
TalentBridge/
│
├── app.py
│
├── database/
│   ├── users.py
│   ├── candidates.py
│   ├── jobs.py
│   ├── candidate_notes.py
│   ├── crm.py
│   ├── rankings.py
│   ├── activity_logs.py
│   └── supabase_client.py
│
├── services/
│   ├── ai_assistant.py
│   ├── candidate_matcher.py
│   ├── ats_score.py
│   ├── cv_parser.py
│   ├── email_generator.py
│   ├── interview_reminders.py
│   ├── ranking_engine.py
│   └── pdf_reports.py
│
├── assets/
│   ├── css/
│   ├── images/
│   └── icons/
│
├── .streamlit/
│   └── secrets.toml
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/TalentBridge.git
cd TalentBridge
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create:

```text
.streamlit/secrets.toml
```

Example:

```toml
SUPABASE_URL="your_supabase_url"
SUPABASE_KEY="your_supabase_key"

OPENAI_API_KEY="your_openai_api_key"

SMTP_SERVER="smtp.gmail.com"
SMTP_PORT="587"
SMTP_EMAIL="your_email@gmail.com"
SMTP_PASSWORD="your_app_password"
```

---

## 🗄️ Database Schema

### app_users

```sql
id
username
password_hash
role
is_active
created_at
```

### candidates

```sql
id
name
email
phone
country
skills
experience_years
status
pipeline_stage
created_at
```

### jobs

```sql
id
title
company
location
description
status
created_at
```

### candidate_notes

```sql
id
candidate_id
note
created_by
created_at
```

### crm_companies

```sql
id
company_name
industry
contact_person
email
phone
created_at
```

### candidate_rankings

```sql
id
candidate_id
job_id
score
reason
created_at
```

### activity_logs

```sql
id
username
role
action
entity_type
entity_id
details
created_at
```

---

## 🔐 User Roles

### Admin

Full Access:

- User Management
- Candidates
- Jobs
- CRM
- Rankings
- Reports
- Activity Logs
- Settings

---

### Recruiter

Access To:

- Candidates
- Jobs
- CRM
- Notes
- Rankings
- Reports
- Email Tools

Restrictions:

- Cannot manage users
- Cannot access system settings

---

### Manager

Access To:

- Dashboard
- Analytics
- Reports
- Candidates
- Jobs

Restrictions:

- Read-only access
- No user management

---

## 🚀 Deployment

### Streamlit Community Cloud

1. Push project to GitHub

```bash
git push origin main
```

2. Create a Streamlit Cloud application

3. Connect GitHub repository

4. Add secrets

5. Deploy

---

## 📈 Roadmap

### Version 2

- Drag & Drop Pipeline
- Advanced Analytics
- Resume Parsing Improvements
- Multi-Tenant SaaS
- Docker Deployment
- Recruiter Performance Tracking
- Public Demo Website

### Version 3

- LinkedIn Integration
- WhatsApp Notifications
- Calendar Integration
- AI Candidate Recommendations
- AI Job Description Generator

---

## 📸 Screenshots

### Dashboard

- Recruitment KPIs
- Analytics
- Hiring Metrics

### Candidate Management

- Candidate Profiles
- Candidate Notes
- Pipeline Tracking

### Recruitment CRM

- Companies
- Contacts
- Relationship Management

### AI Features

- AI Assistant
- Candidate Ranking
- ATS Analysis

---

## 👨‍💻 Author

### TalentBridge

AI-Powered Recruitment Intelligence Platform

Built using:

- Python
- Streamlit
- Supabase
- PostgreSQL
- OpenAI

---

## 📜 License

MIT License

Copyright © 2026 TalentBridge

---

# Version

```text
TalentBridge v1.0.0
```

### Status

✅ Production Ready MVP  
✅ Streamlit Cloud Deployment  
✅ Supabase Connected  
✅ Role-Based Access Control  
✅ Recruitment CRM  
✅ AI Candidate Ranking  
✅ PDF Reports  
✅ Activity Logs  
✅ Interview Reminder Emails  
✅ GitHub Integrated