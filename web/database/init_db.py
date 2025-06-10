import sqlite3

def init_db():
    conn = sqlite3.connect("base.db", check_same_thread=False)
    curseur = conn.cursor()

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS ref (
        id TEXT PRIMARY KEY
    );
    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ref_id TEXT,
        contenu TEXT,
        FOREIGN KEY (ref_id) REFERENCES ref(id)
    );
    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS etats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ref_id TEXT NOT NULL,
        position INTEGER NOT NULL,
        has_box INTEGER NOT NULL CHECK (has_box IN (0, 1)),
        objectif TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ref_id) REFERENCES ref(id)
    );
    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ref_id TEXT NOT NULL,
        action TEXT NOT NULL,
        position INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ref_id) REFERENCES ref(id)
    );
    """)
    conn.commit()
    conn.close()
