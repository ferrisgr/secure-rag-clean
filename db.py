import sqlite3
from datetime import datetime

DB_NAME = "logs.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS query_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    role TEXT,
                    question TEXT,
                    answer TEXT,
                    source_docs TEXT
                )''')
    conn.commit()
    conn.close()

def log_query(role, question, answer, source_docs):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO query_logs (timestamp, role, question, answer, source_docs) VALUES (?, ?, ?, ?, ?)", 
              (datetime.utcnow().isoformat(), role, question, answer, str(source_docs)))
    conn.commit()
    conn.close()

def get_logs(limit=20):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT timestamp, role, question, answer FROM query_logs ORDER BY id DESC LIMIT ?", (limit,))
    logs = c.fetchall()
    conn.close()
    return logs
