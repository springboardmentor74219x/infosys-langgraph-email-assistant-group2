import sqlite3
import json

conn = sqlite3.connect("memory.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    user TEXT PRIMARY KEY,
    data TEXT
)
""")
conn.commit()


def save_memory(user, data):
    cursor.execute(
        "REPLACE INTO memory (user, data) VALUES (?, ?)",
        (user, json.dumps(data))
    )
    conn.commit()


def get_memory(user):
    cursor.execute("SELECT data FROM memory WHERE user=?", (user,))
    row = cursor.fetchone()
    return json.loads(row[0]) if row else {}
