import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "memory.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE,
    value TEXT
)
""")
conn.commit()


def extract_memory(text):
    text = text.lower()

    if "my name is" in text:
        value = text.replace("my name is", "").strip()
        cursor.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", ("name", value))
        conn.commit()
        return f"Your name is {value}"

    if "i love" in text:
        value = text.replace("i love", "").strip()
        cursor.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", ("love", value))
        conn.commit()
        return f"You love {value}"

    if "my role is" in text:
        value = text.replace("my role is", "").strip()
        cursor.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", ("role", value))
        conn.commit()
        return f"Your role is {value}"

    return None


def recall_memory(text):
    text = text.lower()

    if "what is my name" in text or "who am i" in text:
        cursor.execute("SELECT value FROM memory WHERE key='name'")
        row = cursor.fetchone()
        if row:
            return f"Your name is {row[0]}"

    if "what do i love" in text or "what i love" in text:
        cursor.execute("SELECT value FROM memory WHERE key='love'")
        row = cursor.fetchone()
        if row:
            return f"You love {row[0]}"

    if "what is my role" in text or "my role" in text:
        cursor.execute("SELECT value FROM memory WHERE key='role'")
        row = cursor.fetchone()
        if row:
            return f"Your role is {row[0]}"

    return None
