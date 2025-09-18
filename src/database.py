import sqlite3
import config

DB_NAME = config.DB_PATH

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    c.execute("SELECT COUNT(*) FROM scores")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO scores (name, score) VALUES (?, ?)", ("NoName", 0))
    conn.commit()
    conn.close()

def get_high_score():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 1")
    result = c.fetchone()
    conn.close()
    return result if result else ("NoName", 0)

def update_high_score(name, score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    conn.close()
