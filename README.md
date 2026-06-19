# TalentBridge

AI-Powered Recruitment Intelligence Platform built with Streamlit, Supabase, and OpenAI.

TalentBridge helps recruiters manage candidates, job offers, interviews, client communications, ATS analysis, CV parsing, and AI-powered recruitment workflows from a single dashboard.

---

## Features

### Candidate Management
- Add, edit, and manage candidates
- Candidate profiles
- Candidate matching engine
- Candidate timeline tracking
- Pipeline management

### Job Management
- Manage job offers
- Online job search integration
- Job analysis and scoring

### AI Recruitment Tools
- AI Assistant
- CV Parser
- ATS Score Calculator
- Cover Letter Generator
- Candidate Recommendation Engine
- Interview Question Generator

### Interview Management
- Interview Scheduler
- Interview Invitation Email Generator
- Email Sending Integration
- Interview Scorecards

### Client Communication Agent
- Delay Message Generator
- Progress Update Generator
- Client Records Management
- Client CRUD Operations

### Analytics Dashboard
- Recruitment KPIs
- Candidate Pipeline Distribution
- Candidate Status Analytics
- Country Analytics
- Interview Analytics

### Authentication
- Secure Login Page
- Streamlit Secrets Authentication
- Protected Access to Platform

---

## Technology Stack

### Frontend
- Streamlit

### Backend
- Python

### Database
- Supabase

### AI Services
- OpenAI API

### Email Services
- SMTP Email Integration

### Data Processing
- Pandas
- PDF Parsing

---

## Project Structure

```text
TalentBridge/
│
├── assets/
│   ├── images/
│   ├── css/
│   └── main.css
│
├── database/
│
├── models/
│
├── services/
│   ├── auth.py
│   ├── assistant_agent.py
│   ├── ats_score.py
│   ├── candidate_matcher.py
│   ├── client_agent.py
│   ├── cover_letter_generator.py
│   ├── cv_parser.py
│   ├── email_generator.py
│   ├── email_sender.py
│   ├── interview_email.py
│   ├── interview_questions.py
│   ├── interview_scheduler.py
│   ├── pipeline_manager.py
│   ├── recommendation_engine.py
│   ├── resume_reader.py
│   ├── supabase_client.py
│   ├── supabase_manager.py
│   └── ...
│
├── app.py
├── database_manager.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/cold-email_generation-tool.git

cd cold-email_generation-tool
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create:

```text
.streamlit/secrets.toml
```

Example:

```toml
[auth]
admin_username = "admin"
admin_password = "your_secure_password"

[supabase]
url = "YOUR_SUPABASE_URL"
key = "YOUR_SUPABASE_ANON_KEY"

[openai]
api_key = "YOUR_OPENAI_API_KEY"

[email]
smtp_server = "smtp.gmail.com"
smtp_port = 587
email = "your@email.com"
password = "your_app_password"
```

---

## Run Application

```bash
streamlit run app.py
```

Application:

```text
http://localhost:8501
```

---

## Authentication

TalentBridge uses Streamlit Secrets for authentication.

Users must log in before accessing the platform.

Credentials are stored securely in:

```text
.streamlit/secrets.toml
```

This file is excluded from Git using:

```gitignore
.streamlit/
```

---

## Deployment

### Streamlit Community Cloud

1. Push project to GitHub
2. Create Streamlit Cloud account
3. Connect GitHub repository
4. Deploy application
5. Add secrets from:

```toml
[auth]
...

[supabase]
...

[openai]
...

[email]
...
```

inside Streamlit Cloud Secrets Manager.

---

## Security

The following files are excluded from Git:

```gitignore
.streamlit/
.env
venv/
__pycache__/
.vscode/
database/*.db
```

Never commit:

- API Keys
- Supabase Keys
- SMTP Passwords
- Authentication Credentials

---

## Screenshots

### Login Page
- Secure Authentication
- TalentBridge Branding
- Protected Access

### Dashboard
- Recruitment Analytics
- Candidate Metrics
- Hiring KPIs

### AI Tools
- CV Parser
- ATS Scoring
- Cover Letter Generation
- AI Assistant

---

## Author

TalentBridge Recruitment Intelligence Platform

Built with:
- Python
- Streamlit
- Supabase
- OpenAI

---

## License

MIT License