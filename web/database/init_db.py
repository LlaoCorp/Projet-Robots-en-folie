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

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS instructions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        robot_id TEXT NOT NULL,
        blocks LIST NOT NULL,
        statut TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (robot_id) REFERENCES ref(id)
    );
    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        robot_id TEXT NOT NULL,
        vitesse_instant REAL,
        ds_ultrasons REAL,
        status_deplacement TEXT,
        ligne INTEGER,
        status_pince INTEGER CHECK (status_pince IN (0, 1)),
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (robot_id) REFERENCES ref(id)
    );
    """)

    curseur.execute("""
    CREATE TABLE IF NOT EXISTS summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        robot_id TEXT NOT NULL,
        vitesse_moy REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (robot_id) REFERENCES ref(id)
    );
    """)

    conn.commit()
    conn.close()
