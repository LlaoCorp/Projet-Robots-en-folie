# Projet Robots en folie

## 1. Contexte et Objectifs

Ce projet d'intégration a pour objectif la conception et la réalisation d’un robot autonome capable de déplacer des cubes sur une aire de jeu définie. Il mobilise les compétences acquises tout au long de l’année : conception mécanique, électronique, programmation embarquée, développement web et gestion de projet.

L’enjeu principal est de concevoir une solution fonctionnelle, modulaire et présentable, en équipe, avec une gestion rigoureuse et une démonstration finale professionnelle.

---

## 2. Équipe et Gestion de Projet

* **Équipe** : Alexandre Chabre, Hugo Ruiz--Passelande, Valentin Llao.
* **Méthodologie** : Approche agile (scrums quotidiens, rétrospectives régulières).
* **Outils collaboratifs** : Trello, GitHub, Google Drive.
* **Livrables documentaires** :

  * Compte-rendus de réunions
  * Auto-évaluations régulières
  * Diagrammes de Gantt
  * Documentation technique (README, commentaires, Doxygen)
* **Jalons clés** :

  * Jalon 0 : Présentation initiale du projet (2 juin)
  * Jalon 1 : Modélisation et validation des choix techniques (6 juin)
  * Jalon 2 : Première version fonctionnelle (12 juin)
  * Jalon 3 : Livraison finale avec démonstration (19 juin)
  * Jalon 4 : Soutenance orale (20 juin)

---

## 3. Cahier des Charges Fonctionnel

### 3.1 Robot

* Navigation autonome ou téléopérée sur surface plane
* Identification, saisie et transport de cubes
* Communication WiFi avec une console de contrôle
* Envoi d’informations de position, état et mission

### 3.2 Pince

* Ouverture et fermeture via servomoteur
* Préhension fiable des cubes
* Résistance mécanique testée

### 3.3 Logiciel embarqué

* Lecture des capteurs (IR, ultrasons)
* Contrôle des moteurs et de la pince
* Communication bidirectionnelle avec le serveur (WiFi)
* Implémentation en MicroPython (ESP32)

### 3.4 Console de Contrôle

* Interface Tkinter pour PC
* Affichage en temps réel des données du robot
* Envoi de missions personnalisées
* Affichage des messages et alertes

### 3.5 Console de Simulation

* Interface Java Swing pour simuler les mouvements du robot
* Visualisation graphique de la position et orientation
* Interaction avec le serveur via API

### 3.6 Serveur Web

* API REST en FastAPI
* Base de données SQLite
* Interface web simple pour le suivi des missions

---

## 4. Matériel et Environnement

* **Microcontrôleur** : ESP32
* **Capteurs** : Capteurs de ligne IR, ultrasons
* **Actionneurs** : Moteurs DC, servomoteur (pince)
* **Outils logiciels** :

  * MicroPython (robot)
  * Python 3.10+ (FastAPI, Tkinter)
  * Java Swing (simulateur)
  * CAO : SolidWorks / Fusion 360
  * Fabrication : impression 3D, découpe laser

---

## 5. Réalisation Mécanique

### 5.1 Étude technique

* Analyse de différentes mécaniques de pinces
* Choix d’un modèle à pince parallèle motorisée

### 5.2 CAO

* Dimensions : 150x150x150 mm max
* Conception des pièces via SolidWorks
* Export en STL et DXF pour impression et découpe

### 5.3 Fabrication

* Impression 3D (PLA)
* Découpe laser des supports MDF
* Assemblage mécanique avec visserie

---

## 6. Programmation MicroPython (ESP32)

### 6.1 Gestion des entrées/sorties

* Utilisation des modules `machine.PWM` et `machine.Pin`
* Mappage clair des broches (documentation Doxygen)

### 6.2 Réseau et communication

* Connexion WiFi automatique
* Communication via MQTT ou sockets (selon versions)
* Interaction avec le serveur FastAPI : missions, télémétries

---

## 7. Serveur Web (FastAPI)

### 7.1 Architecture

* **main.py** : point d’entrée de l’application
* **database/** : gestion des modèles, base SQLite
* **routes/** : endpoints de l’API (création robot, missions...)
* **web/templates/** : interface web simple (HTML/CSS)

### 7.2 Lancement rapide

```bash
pip install fastapi uvicorn
python database/init_db.py
uvicorn main:app --reload
```

Accès à : [http://localhost:8000](http://localhost:8000)

### 7.3 Exemple de route

```python
@app.get("/robots/{robot_id}")
async def get_robot(robot_id: str):
    return {"id": robot_id, "status": "active"}
```

---

## 8. Console de Contrôle (Tkinter)

* Fenêtre principale avec champs d’identification
* Envoi de blocs-missions en un clic
* Suivi en direct de la télémétrie
* Affichage des journaux d’exécution

---

## 9. Console de Simulation (Java)

* Simulation de la position du robot
* Réception des missions via API
* Visualisation graphique simple

---

## 10. Base de Données SQLite

* **robots** : ID, nom, position, statut
* **missions** : instructions, timestamps, robot\_id
* **summary** : état final et durée
* Historique des événements enregistrés

---

## 11. Documentation et Présentation

* Documentation du code (Doxygen)
* Journaux de suivi journalier
* Diagrammes (Gantt, architecture)
* Vidéo finale de démonstration
* Soutenance orale (15 min)

---

## 12. Limites et pistes d’amélioration

* Délai entre détection ligne et réaction moteur à optimiser
* Amélioration de la consommation énergétique
* Étendre le système à plusieurs robots simultanés
* Interface web plus complète (dashboard en WebSocket)

---

## 13. Ressources utiles

* **Référents pédagogiques** : M. Madeline, M. Delcombel, Mme. Dolle-Fabre
* MicroPython : [https://docs.micropython.org](https://docs.micropython.org)
* FastAPI : [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
* SQLite : [https://sqlite.org/index.html](https://sqlite.org/index.html)
* ChatGPT : [https://chatgpt.com](https://chatgpt.com)