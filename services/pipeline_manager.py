import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "talentbridge.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def update_candidate_stage(candidate_id, new_stage):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE candidates
        SET pipeline_stage = ?
        WHERE id = ?
        """,
        (new_stage, candidate_id)
    )

    conn.commit()
    conn.close()