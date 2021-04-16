import sqlite3
import json
from models import Entry


def get_all_entries():
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            e.date,
            e.concept,
            e.text,
            e.mood_id
        FROM Entry e
        """)
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry = Entry(row['id'], row['date'], row['concept'],
                            row['text'], row['mood_id'])
            entries.append(entry.__dict__)
    return json.dumps(entries)
