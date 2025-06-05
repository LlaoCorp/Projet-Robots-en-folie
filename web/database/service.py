import sqlite3
import uuid

def get_db():
    return sqlite3.connect("base.db")

def create_robot(name: str):
    robot_id = str(uuid.uuid4())
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ref (id) VALUES (?)", (robot_id,))
    conn.commit()
    conn.close()
    return robot_id

def get_mission(ref_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM missions WHERE ref_id = ?", (ref_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def list_missions():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM missions")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def ajouter_message(ref_id, contenu):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ref WHERE id = ?", (ref_id))
    if cursor.fetchone()[0] != 0:
        cursor.execute("INSERT INTO ref (id) VALUES (?)", (ref_id))
    cursor.execute("INSERT INTO messages (ref_id, contenu) VALUES (?, ?)", (ref_id, contenu))
    conn.commit()

def recuperer_messages():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ref_id, contenu FROM messages")
    return [{"ref_id": row[0], "contenu": row[1]} for row in cursor.fetchall()]