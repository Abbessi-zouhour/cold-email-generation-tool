import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "talentbridge.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_interviews_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            candidate_name TEXT,
            candidate_email TEXT,
            job_title TEXT,
            company TEXT,
            interview_date TEXT,
            interview_time TEXT,
            interview_type TEXT,
            notes TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_interview(
    candidate_id,
    candidate_name,
    candidate_email,
    job_title,
    company,
    interview_date,
    interview_time,
    interview_type,
    notes,
    status="Scheduled"
):
    create_interviews_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO interviews (
            candidate_id,
            candidate_name,
            candidate_email,
            job_title,
            company,
            interview_date,
            interview_time,
            interview_type,
            notes,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_id,
        candidate_name,
        candidate_email,
        job_title,
        company,
        str(interview_date),
        str(interview_time),
        interview_type,
        notes,
        status
    ))

    conn.commit()
    conn.close()


def get_interviews():
    create_interviews_table()

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM interviews ORDER BY interview_date DESC", conn)
    conn.close()

    return df


def delete_interview(interview_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM interviews WHERE id = ?", (interview_id,))

    conn.commit()
    conn.close()