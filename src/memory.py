import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "memory.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()


# ✅ Create memory table
cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE,
    value TEXT
)
""")
conn.commit()

# ✅ Store memory rules
def extract_memory(text):
    text = text.lower()

    if "my name is" in text:
        value = text.replace("my name is", "").strip()
        cursor.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", ("name", value))
        conn.commit()
        return f"Got it! I will remember your name is {value}."

    if "i love" in text:
        value = text.replace("i love", "").strip()
        cursor.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", ("love", value))
        conn.commit()
        return f"Nice! I will remember that you love {value}."

    return None


# ✅ Retrieve memory rules
def recall_memory(text):
    text = text.lower()

    if "what is my name" in text or "who am i" in text:
        cursor.execute("SELECT value FROM memory WHERE key = 'name'")
        row = cursor.fetchone()
        if row:
            return f"Your name is {row[0]}"

    if "what do i love" in text or "who do i love" in text or "favorite god" in text:
        cursor.execute("SELECT value FROM memory WHERE key = 'love'")
        row = cursor.fetchone()
        if row:
            return f"You love {row[0]}"

    return None
