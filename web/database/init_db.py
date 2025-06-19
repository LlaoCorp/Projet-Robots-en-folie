##
# @file init_db.py
# @brief Initialise la base de données SQLite avec toutes les tables nécessaires au simulateur de robot.
#
# Ce fichier contient une seule fonction `init_db()` qui crée les tables si elles n'existent pas :
# - ref : robots enregistrés
# - messages : messages textuels associés à un robot
# - instructions : missions assignées aux robots
# - telemetry : données de télémétrie envoyées par les robots
# - summary : résumés de missions complétées

import sqlite3

##
# @brief Initialise la base de données SQLite avec les tables nécessaires au bon fonctionnement de l'API.
#
# Crée les tables :
# - `ref` : contient les robots
# - `messages` : messages associés à chaque robot
# - `instructions` : missions (blocs à récupérer) assignées
# - `telemetry` : données de capteurs en temps réel
# - `summary` : fin de mission
def init_db():
    conn = sqlite3.connect("base.db", check_same_thread=False)
    curseur = conn.cursor()

    # Table des robots (références)
    curseur.execute("""
    CREATE TABLE IF NOT EXISTS ref (
        id TEXT PRIMARY KEY,
        name TEXT
    );
    """)

    # Table des messages associés à un robot
    curseur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ref_id TEXT,
        contenu TEXT,
        FOREIGN KEY (ref_id) REFERENCES ref(id)
    );
    """)

    # Table des instructions données à un robot
    curseur.execute("""
    CREATE TABLE IF NOT EXISTS instructions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        robot_id TEXT NOT NULL,
        blocks LIST NOT NULL,
        status TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (robot_id) REFERENCES ref(id)
    );
    """)

    # Table des données de télémétrie (capteurs) du robot
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

    # Table des résumés de mission envoyés par le robot
    curseur.execute("""
    CREATE TABLE IF NOT EXISTS summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        robot_id TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (robot_id) REFERENCES ref(id)
    );
    """)

    conn.commit()
    conn.close()
