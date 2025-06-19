## @file service.py
#  @brief Fonctions de service pour la manipulation de la base de données SQLite.
#  Fournit des opérations CRUD pour les robots, les instructions, la télémétrie,
#  les résumés, les messages et les statistiques de missions.

import sqlite3

## @brief Établit une connexion à la base de données.
#  @return Connexion SQLite3

def get_db():
    return sqlite3.connect("base.db")

## @brief Crée un nouveau robot dans la base si l'ID n'existe pas.
#  @param id Identifiant unique du robot
#  @param name Nom du robot
#  @return True si créé, False si ID existe déjà

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

## @brief Enregistre une instruction pour un robot existant.
#  @param robot_id ID du robot
#  @param blocks Liste des blocs (str)
#  @param status Statut de l'instruction (ex: 'new')
#  @return True si succès, False si robot introuvable

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

## @brief Récupère la dernière instruction avec statut 'new' pour un robot.
#  @param robot_id ID du robot
#  @return Dictionnaire avec instruction ou None

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

## @brief Récupère toutes les instructions pour un robot.
#  @param robot_id ID du robot
#  @return Liste d'instructions

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

## @brief Change le statut de la dernière instruction 'new' d’un robot.
#  @param robot_id ID du robot
#  @param status Nouveau statut à appliquer
#  @return True si modification effectuée, False sinon

def changer_status_instruction(robot_id: str, status: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE instructions
        SET status = ?
        WHERE robot_id = ?
        AND id = (SELECT id FROM instructions WHERE robot_id = ? AND status ='new' ORDER BY id DESC LIMIT 1)
    """, (status, robot_id, robot_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0

## @brief Enregistre une entrée de télémétrie pour un robot.
#  @param telemetry Données de télémétrie (objet avec attributs)

def enregistrer_telemetry(telemetry):
    print(telemetry)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO telemetry (robot_id, vitesse_instant, ds_ultrasons, status_deplacement, ligne, status_pince)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (telemetry.robot_id, telemetry.vitesse_instant, telemetry.ds_ultrasons, telemetry.statut_deplacement, telemetry.ligne, telemetry.statut_pince))
    conn.commit()
    conn.close()

## @brief Récupère la dernière télémétrie d’un robot.
#  @param robot_id ID du robot
#  @return Dictionnaire des données ou None

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

## @brief Enregistre un résumé de mission pour un robot.
#  @param summary Objet contenant l'ID du robot

def enregistrer_summary(summary):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO summary (robot_id)
        VALUES (?)
    """, (summary.robot_id,))
    conn.commit()
    conn.close()

##
# @brief Ajoute un message dans la table de test `messages`.
# @param ref_id ID du robot.
# @param contenu Message à enregistrer.

def ajouter_message(ref_id, contenu):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (ref_id, contenu) VALUES (?, ?)", (ref_id, contenu))
    conn.commit()
    conn.close()

##
# @brief Récupère tous les messages (utilisé pour les tests).
# @return Liste de messages sous forme de dictionnaires.

def recuperer_messages():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ref_id, contenu FROM messages")
    return [{"ref_id": row[0], "contenu": row[1]} for row in cursor.fetchall()]

## @brief Récupère la durée des missions déjà exécutées utilisé dans une idée de réalisation des bonus.
#  @param robot_id ID du robot
#  @return Liste de durées (secondes)

def recuperer_temps_missions(robot_id: str):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT duree
            FROM instructions
            WHERE robot_id = ? AND duree IS NOT NULL
            ORDER BY id ASC
        """, (robot_id,))
        rows = cursor.fetchall()
        return [row[0] for row in rows if row[0] is not None]
    finally:
        conn.close()
