import sqlite3

conn = sqlite3.connect("base.db", check_same_thread=False)
curseur = conn.cursor()

curseur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ref_id TEXT,
    contenu TEXT
)
""")
conn.commit()

def ajouter_message(ref_id, contenu):
    curseur.execute("INSERT INTO messages (ref_id, contenu) VALUES (?, ?)", (ref_id, contenu))
    conn.commit()

def recuperer_messages():
    curseur.execute("SELECT ref_id, contenu FROM messages")
    return [{"ref_id": row[0], "contenu": row[1]} for row in curseur.fetchall()]
