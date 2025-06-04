import sqlite3

conn = sqlite3.connect("base.db", check_same_thread=False)
curseur = conn.cursor()

curseur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ref_id SECONDARY KEY,
    contenu TEXT,
    FOREIGN KEY (ref_id) REFERENCES ref(id)
)
CREATE TABLE IF NOT EXISTS ref (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
)
""")
conn.commit()

def ajouter_message(ref_id, contenu):
    curseur.execute("SELECT COUNT(*) FROM ref WHERE id = ?", (ref_id))
    if curseur.fetchone()[0] != 0:
        curseur.execute("INSERT INTO ref (id) VALUES (?)", (ref_id))
    curseur.execute("INSERT INTO messages (ref_id, contenu) VALUES (?, ?)", (ref_id, contenu))
    conn.commit()

def recuperer_messages():
    curseur.execute("SELECT ref_id, contenu FROM messages")
    return [{"ref_id": row[0], "contenu": row[1]} for row in curseur.fetchall()]
