import sqlite3
import config


def _connect():
    return sqlite3.connect(config.DB_PATH)


def init_db():
    with _connect() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        ''')
    conn.close()


def get_top_scores(limit):
    """Best scores first. Zero scores (like the old 'NoName' placeholder row) are skipped."""
    conn = _connect()
    rows = conn.execute(
        "SELECT TRIM(name), score FROM scores WHERE score > 0 "
        "ORDER BY score DESC, id ASC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return rows


def makes_scoreboard(score):
    """True if this score is good enough to appear on the scoreboard."""
    if score <= 0:
        return False
    top = get_top_scores(config.SCOREBOARD_ROWS)
    return len(top) < config.SCOREBOARD_ROWS or score > top[-1][1]


def add_score(name, score):
    with _connect() as conn:
        conn.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name.strip(), score))
    conn.close()
