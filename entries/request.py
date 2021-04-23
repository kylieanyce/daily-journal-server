import sqlite3
import json
from models import Entry
from models import Mood


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
            e.mood_id,
            m.label
        FROM Entry e
        JOIN Mood m
            ON m.id = e.mood_id
        """)
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry = Entry(row['id'], row['date'], row['concept'],
                            row['text'], row['mood_id'])
            mood = Mood(row['id'], row['label'])

            entry.mood = mood.__dict__
            entries.append(entry.__dict__)
    return json.dumps(entries)


def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.date,
            e.concept,
            e.text,
            e.mood_id
        FROM Entry e
        WHERE e.id = ?
        """, (id, ))
        # Load the single result into memory
        data = db_cursor.fetchone()
        # Create an animal instance from the current row
        entry = Entry(data['id'], data['date'], data['concept'],
                        data['text'], data['mood_id'])
        return json.dumps(entry.__dict__)


def get_entry_by_search(search_term):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.date,
            e.concept,
            e.text,
            e.mood_id,
            m.label
        FROM Entry e
        JOIN Mood m
            ON m.id = e.mood_id
        WHERE e.text LIKE ?
        """, (f'%{search_term}%', ))
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry = Entry(row['id'], row['date'], row['concept'],
                            row['text'], row['mood_id'])
            mood = Mood(row['id'], row['label'])

            entry.mood = mood.__dict__
            entries.append(entry.__dict__)
    return json.dumps(entries)


def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entry
            ( date, concept, text, mood_id )
        VALUES
            ( ?, ?, ?, ? );
        """, (new_entry['date'], 
            new_entry['concept'], 
            new_entry['text'], 
            new_entry['mood_id']))

        id = db_cursor.lastrowid
        new_entry['id'] = id

        for tag in new_entry['tag_id']:
            db_cursor.execute("""
            INSERT INTO entry_tag    
                (entry_id, tag_id)
            VALUES (?, ?);
            """, (id, tag))
    return json.dumps(new_entry)


def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Entry
            SET
                date = ?,
                concept = ?,
                text = ?,
                mood_id = ?
        WHERE id = ?
        """, (new_entry['date'], 
            new_entry['concept'], 
            new_entry['text'], 
            new_entry['mood_id'], id, ))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True


def delete_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM entry
        WHERE id = ?
        """, (id, ))