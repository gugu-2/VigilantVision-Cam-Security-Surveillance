import sqlite3

def init_db():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            faces_detected INTEGER,
            threats_detected INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_log(faces, threats):
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (faces_detected, threats_detected) VALUES (?, ?)",
        (faces, threats)
    )
    conn.commit()
    conn.close()

init_db()