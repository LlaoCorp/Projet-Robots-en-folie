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

def enregistrer_instruction(robot_id: str, blocks: list, statut: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ref WHERE id = ?", (robot_id,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO ref (id) VALUES (?)", (robot_id,))
    cursor.execute("""
        INSERT INTO instructions (robot_id, blocks, statut)
        VALUES (?, ?, ?)
    """, (robot_id, str(blocks), statut))
    conn.commit()
    conn.close()

def get_current_instruction(robot_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT blocks, statut
        FROM instructions
        WHERE robot_id = ? AND statut = 'new'
        ORDER BY id DESC
        LIMIT 1
    """, (robot_id,))
    row = cursor.fetchone()
    if row:
        return {"robot_id": robot_id, "blocks": row[0], "statut": row[1]}
    return None

def changer_statut_instruction(robot_id: str, statut: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE instructions
        SET statut = ?
        WHERE robot_id = ?
        AND id = (SELECT id FROM instructions WHERE robot_id = ? ORDER BY id DESC LIMIT 1)
    """, (statut, robot_id, robot_id))
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

def enregistrer_summary(summary):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO summary (robot_id, vitesse_moy)
        VALUES (?, ?)
    """, (summary.robot_id, summary.vitesse_moy))
    conn.commit()
    conn.close()

def ajouter_message(ref_id, contenu):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ref WHERE id = ?", (ref_id,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO ref (id) VALUES (?)", (ref_id,))
    cursor.execute("INSERT INTO messages (ref_id, contenu) VALUES (?, ?)", (ref_id, contenu))
    conn.commit()
    conn.close()

def recuperer_messages():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ref_id, contenu FROM messages")
    return [{"ref_id": row[0], "contenu": row[1]} for row in cursor.fetchall()]

def enregistrer_etat_robot(etat):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO etats (ref_id, position, has_box, objectif)
        VALUES (?, ?, ?, ?)
    """, (etat.ref_id, etat.position, int(etat.has_box), etat.objectif))
    conn.commit()

def get_etats(ref_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT objectif FROM etats WHERE ref_id = ?", (ref_id,))
    etats = cursor.fetchall()
    conn.close()
    return [{"objectif": row[0]} for row in etats]
    
def get_actions(ref_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT action FROM actions WHERE ref_id = ?", (ref_id,))
    actions = cursor.fetchall()
    conn.close()
    return [{"action": row[0]} for row in actions]

def ajouter_action_en_base(action):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO actions (ref_id, action, position)
        VALUES (?, ?, ?)
    """, (action.ref_id, action.action, action.position))
    conn.commit()

def enregistrer_robot(data):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ref (id)
        VALUES (?)
        ON CONFLICT(id) DO NOTHING
    """, (data.ref_id,))
    cursor.execute("""
        INSERT INTO etats (ref_id, position, has_box, objectif)
        VALUES (?, ?, ?, ?)
    """, (data.ref_id, data.position, int(data.has_box), "Initialisation"))
    conn.commit()