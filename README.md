# Projet Robots en folie

## 1. Contexte et Objectifs

Ce projet d'intégration a pour objectif la conception et la réalisation d’un robot transporteur autonome capable de déplacer des cubes sur une aire de jeu définie.
Il permet d’appliquer les compétences techniques au cours de l'année : mécanique, électronique, programmation embarquée et développement web.

L’enjeu est de mener à bien un projet multidisciplinaire, de la conception à la démonstration finale, en travaillant en équipe, avec une gestion rigoureuse et un rendu professionnel.

---

## 2. Équipe et Gestion de Projet

* **Composition** : Alexandre Chabre, Hugo Ruiz--Passelande et Valentin Llao.
* **Méthodologie** : Agile, avec réunions quotidiennes courtes.
* **Suivi** : Tableau de tâches partagé (Trello, GitHub et Google Drive).
* **Documentation** :

  * Compte-rendus de réunions.
  * Auto-évaluations
  * Diagrammes de Gantt.
  * Documentation technique (README, commentaires, Doxygen).
* **Jalons** :

  * Jalon 0 : Spécifications, choix techniques.
  * Jalon 1 : Architecture logicielle, prototypes.
  * Jalon 2 : Intégration des modules et tests.
  * Jalon 3 : Démonstration publique.

---

## 3. Architecture du Projet

Le projet est divisé en plusieurs modules interconnectés :

* **Serveur FastAPI** : gère la base de données SQLite, les routes d'échange entre l'interface web, les robots, et l'API REST.
* **Base de données** : stocke les instructions, télémétries, résumés de mission, et messages.
* **Interface Web** : accessible dans `web/templates/index.html` pour créer un robot et consulter les missions.
* **Code embarqué MicroPython** : le robot interagit avec le serveur, exécute les missions et renvoie des télémétries.

> ⚠️ Le code MicroPython peut évoluer selon les composants matériels ou tests sur le robot.

---

## 4. Structure du Projet

```
Projet-Robots-en-folie/
├── database/
│   ├── base_model.py            # Modèles de données Pydantic
│   ├── init_db.py               # Création des tables SQLite
│   └── service.py               # Fonctions d'accès à la base
│
├── web/
│   ├── templates/
│   │   └── index.html        # Interface web utilisateur
│   └── static/
│       └── styles.css           # Styles CSS de l'interface
│
├── routes/
│   └── main.py                 # Routes FastAPI principales
│
├── micropython/                  # Code embarqué à flasher dans le robot
├── base.db                      # Base de données SQLite (après initialisation)
├── README.md
└── main.py                   # Lancement du serveur FastAPI
```

---

## 5. Lancement rapide

### Prérequis

* Python 3.10+
* FastAPI
* Uvicorn

### Installation des dépendances

```bash
pip install fastapi uvicorn
```

### Initialisation de la base de données

```bash
python database/init_db.py
```

### Démarrage du serveur

```bash
uvicorn main:app --reload
```

Puis accéder à l'interface web : [http://localhost:8000](http://localhost:8000)

---

## 6. Fonctionnalités clés

* Création dynamique de robots via formulaire.
* Envoi et consultation des missions.
* Récupération des télémétries robot en temps réel.
* Mise à jour du statut des missions.
* Architecture REST propre pour interfaçage robot/serveur.

---

## 7. Améliorations possibles

* Ajout d'une authentification JWT pour sécuriser l'interface.
* Tableau de bord temps réel avec WebSocket.
* Gestion des logs par robot.
* Export CSV des données télémétriques.

---

## 8. Remarques

Le projet est conçu pour être modulaire. Le code embarqué MicroPython peut être adapté en fonction de l'évolution du châssis, des capteurs, ou des stratégies de mission. Les interfaces et routes sont stables et adaptées à une communication fiable entre le robot et le serveur.
