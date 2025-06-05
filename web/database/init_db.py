import sqlite3

def init_db():
    conn = sqlite3.connect("base.db", check_same_thread=False)
    curseur = conn.cursor()

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS ref (
        id INTEGER PRIMARY KEY
    )
    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS missions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ref_id TEXT,
        description TEXT,
        FOREIGN KEY (ref_id) REFERENCES ref(id)
    )
    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ref_id INTEGER,
        contenu TEXT,
        FOREIGN KEY (ref_id) REFERENCES ref(id)
    )
    """)
    conn.commit()
    conn.close()
