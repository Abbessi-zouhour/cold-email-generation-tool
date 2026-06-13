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


if __name__ == "__main__":
    initialize_database()
    print("Database created successfully.")
