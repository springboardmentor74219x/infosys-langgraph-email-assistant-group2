import sqlite3

DB_FILE = "memory.db"

def init_memory():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()

def load_memory():
    init_memory()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM memory")
    rows = cursor.fetchall()
    conn.close()
    return {key: value for key, value in rows}

def update_memory(key, value):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO memory (key, value)
        VALUES (?, ?)
    """, (key, value))
    conn.commit()
    conn.close()