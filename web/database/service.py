import sqlite3
import uuid

def get_db():
    return sqlite3.connect("base.db")

def create_robot(id: str, name: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ref WHERE id = ?", (id,))
    if cursor.fetchone()[0] > 0:
        return False
    cursor.execute("INSERT INTO ref (id, name) VALUES (?, ?)", (id, name))
    conn.commit()
    conn.close()
    return True

def enregistrer_instruction(robot_id: str, blocks: list, status: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ref WHERE id = ?", (robot_id,))
    if cursor.fetchone()[0] == 0:
        return False
    cursor.execute("""
        INSERT INTO instructions (robot_id, blocks, status)
        VALUES (?, ?, ?)
    """, (robot_id, str(blocks), status))
    conn.commit()
    conn.close()
    return True

def get_current_instruction(robot_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT blocks, status
        FROM instructions
        WHERE robot_id = ? AND status = 'new'
        ORDER BY id DESC
        LIMIT 1
    """, (robot_id,))
    row = cursor.fetchone()
    if row:
        return {"robot_id": robot_id, "blocks": row[0], "status": row[1]}
    return None

def get_instructions(robot_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT blocks
        FROM instructions
        WHERE robot_id = ?
        ORDER BY id DESC
    """, (robot_id,))
    rows = cursor.fetchall()
    instructions = [{"blocks": row[0]} for row in rows]
    conn.close()
    return instructions

def changer_status_instruction(robot_id: str, status: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE instructions
        SET status = ?
        WHERE robot_id = ?
        AND id = (SELECT id FROM instructions WHERE robot_id = ? ORDER BY id DESC LIMIT 1)
    """, (status, robot_id, robot_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0

def enregistrer_telemetry(telemetry):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO telemetry (robot_id, vitesse_instant, ds_ultrasons, status_deplacement, ligne, status_pince)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (telemetry.robot_id, telemetry.vitesse_instant, telemetry.ds_ultrasons, telemetry.status_deplacement, telemetry.ligne, int(telemetry.status_pince)))
    conn.commit()
    conn.close()

def recuperer_telemetry(robot_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT vitesse_instant, ds_ultrasons, status_deplacement, ligne, status_pince
        FROM telemetry
        WHERE robot_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (robot_id,))
    row = cursor.fetchone()
    if row:
        return {
            "robot_id": robot_id,
            "vitesse_instant": row[0],
            "ds_ultrasons": row[1],
            "status_deplacement": row[2],
            "ligne": row[3],
            "status_pince": bool(row[4])
        }
    return None

def enregistrer_summary(summary):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO summary (robot_id)
        VALUES (?)
    """, (summary.robot_id,))
    conn.commit()
    conn.close()

def ajouter_message(ref_id, contenu):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (ref_id, contenu) VALUES (?, ?)", (ref_id, contenu))
    conn.commit()
    conn.close()

def recuperer_messages():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ref_id, contenu FROM messages")
    return [{"ref_id": row[0], "contenu": row[1]} for row in cursor.fetchall()]