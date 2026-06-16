import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "talentbridge.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_timeline_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidate_timeline (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        event_date TEXT,
        event_type TEXT,
        notes TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_timeline_event(
    candidate_id,
    event_date,
    event_type,
    notes
):

    create_timeline_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO candidate_timeline (
        candidate_id,
        event_date,
        event_type,
        notes
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        candidate_id,
        event_date,
        event_type,
        notes
    ))

    conn.commit()
    conn.close()


def get_candidate_timeline(candidate_id):

    create_timeline_table()

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM candidate_timeline
        WHERE candidate_id = ?
        ORDER BY event_date DESC, id DESC
        """,
        conn,
        params=(candidate_id,)
    )

    conn.close()

    return df


def delete_timeline_event(event_id):

    create_timeline_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM candidate_timeline WHERE id = ?",
        (event_id,)
    )

    conn.commit()
    conn.close()