import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "database" / "talentbridge.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """Create/refresh SQLite tables from the existing CSV files."""
    conn = get_connection()

    candidates = pd.read_csv(BASE_DIR / "database" / "candidates.csv")
    jobs = pd.read_csv(BASE_DIR / "database" / "jobs.csv")
    clients = pd.read_csv(BASE_DIR / "database" / "clients.csv")

    candidates.to_sql("candidates", conn, if_exists="replace", index=False)
    jobs.to_sql("jobs", conn, if_exists="replace", index=False)
    clients.to_sql("clients", conn, if_exists="replace", index=False)

    conn.close()


def get_candidates():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM candidates", conn)
    conn.close()
    return df


def get_jobs():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM jobs", conn)
    conn.close()
    return df


def get_clients():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM clients", conn)
    conn.close()
    return df


def save_candidates(df):
    conn = get_connection()
    df.to_sql("candidates", conn, if_exists="replace", index=False)
    conn.close()


def save_jobs(df):
    conn = get_connection()
    df.to_sql("jobs", conn, if_exists="replace", index=False)
    conn.close()


def save_clients(df):
    conn = get_connection()
    df.to_sql("clients", conn, if_exists="replace", index=False)
    conn.close()


def add_candidate(name, email, country, experience_years, skills, status, pipeline_stage):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO candidates (
            name,
            email,
            country,
            experience_years,
            skills,
            status,
            pipeline_stage
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        country,
        experience_years,
        skills,
        status,
        pipeline_stage
    ))

    conn.commit()
    conn.close()


def update_candidate(candidate_id, name, email, country, experience_years, skills, status, pipeline_stage):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE candidates
        SET name = ?,
            email = ?,
            country = ?,
            experience_years = ?,
            skills = ?,
            status = ?,
            pipeline_stage = ?
        WHERE id = ?
    """, (
        name,
        email,
        country,
        experience_years,
        skills,
        status,
        pipeline_stage,
        candidate_id
    ))

    conn.commit()
    conn.close()


def delete_candidate(candidate_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM candidates
        WHERE id = ?
    """, (candidate_id,))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()
    print("Database created successfully.")