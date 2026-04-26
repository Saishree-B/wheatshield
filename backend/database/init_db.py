import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "wheatshield.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Users table (optional – future use)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
)
""")

# History table
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    disease TEXT,
    confidence REAL,
    severity TEXT,
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully at:", DB_PATH)
