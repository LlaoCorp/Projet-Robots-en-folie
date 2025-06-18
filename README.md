# Projet Robots en folie

## 1. Contexte et Objectifs

Ce projet d'intégration a pour objectif la conception et la réalisation d’un robot transporteur autonome capable de déplacer des cubes sur une aire de jeu définie.  
Il permet d’appliquer les compétences techniques au cours de l'année : mécanique, électronique, programmation embarquée et développement web.

L’enjeu est de mener à bien un projet multidisciplinaire, de la conception à la démonstration finale, en travaillant en équipe, avec une gestion rigoureuse et un rendu professionnel.

---

## 2. Équipe et Gestion de Projet

- **Composition** : Alexandre Chabre, Hugo Ruiz--Passelande et Valentin Llao.
- **Méthodologie** : Agile, avec réunions quotidiennes courtes.  
- **Suivi** : Tableau de tâches partagé (Trello, GitHub et Google Drive).  
- **Documentation** :  
  - Compte-rendus de réunions.
  - Auto-évaluations
  - Diagrammes de Gantt.
  - Documentation technique (README, commentaires, Doxygen).  
- **Jalons** :  
  - Jalon 0 : Présentation projet (2 juin)
  - Jalon 1 : Modélisation (6 juin)
  - Jalon 2 : Version fonctionnelle 1 (12 juin)
  - Jalon 3 : Livraison finale (19 juin)
  - Jalon 4 : Soutenance orale (20 juin)

---

## 3. Cahier des Charges Fonctionnel

### 3.1 Robot

- Se déplacer sur une surface plane avec une navigation autonome ou pilotée.  
- Identifier, saisir et transporter des cubes placés sur la zone de jeu.  
- Communiquer avec une console de contrôle via WiFi.  
- Retourner des informations de position, état, missions, et alertes.

### 3.2 Pince

- Ouverture et fermeture motorisée (servo).  
- Saisie sécurisée des cubes.
- Résistance mécanique adaptée.

### 3.3 Logiciel embarqué

- Lecture capteurs (ultrasons, ligne).  
- Contrôle moteurs et pince.  
- Communication bidirectionnelle WiFi.  
- Mise en œuvre MicroPython sur ESP32.

### 3.4 Console de contrôle

- Interface utilisateur intuitive (Tkinter).  
- Visualisation en temps réel des données robot.  
- Envoi de commandes (déplacement, mission).  
- Gestion des états et alertes.

### 3.5 Console de simulation

- Simulation graphique du robot (Java Swing).  
- Interaction avec serveur pour tester commandes.

### 3.6 Serveur web

- API REST avec FastAPI.  
- Gestion de la base SQLite.  
- Interface web simple pour suivi et configuration.

---

## 4. Matériel et Environnement

- **Microcontrôleur** : ESP32  
- **Capteurs** : Ultrasons, capteurs de ligne IR  
- **Actionneurs** : Moteurs DC, servomoteur  
- **Outils logiciels** :  
  - MicroPython (ESP32)  
  - Python 3.8+ (FastAPI, Tkinter, SQLite)  
  - Java (Swing pour simulation)  
  - CAO : SolidWorks / Fusion 360  
  - Impression 3D, découpe laser

---

## 5. Réalisation mécanique

### 5.1 Étude préalable

- Analyse de pinces existantes (ex. pince à servo, pince parallèle).  
- Choix du type de préhension (pince parallèle, force requise).

### 5.2 Conception CAO

- Dimensions maxi : 150x150x150 mm.  
- Modélisation en SolidWorks (fichiers STL et DXF).  
- Intégration visserie, fixation servomoteur.

### 5.3 Fabrication

- Impression 3D des pièces plastiques.  
- Découpe laser des supports en MDF.  
- Assemblage et test mécanique.

---

## 6. Programmation MicroPython - Contrôleur ESP32

### 6.1 Configuration des pins

Utilisation de PWM et PIN dans micropython

### 6.2 Communication WiFi et serveur MQTT

- Connexion au réseau WiFi.  
- Publication / abonnement MQTT (ou sockets) pour échanges avec serveur.

---

## 7. Serveur Web FastAPI (Python)

### 7.1 Structure

- **Fichier principal** : main.py  
- **Modules** :  
  - base.py (gestion SQLite)  
  - api/router.py (routes FastAPI)  
  - models.py (définition données)

### 7.2 Exemple route API

    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/robots/{robot_id}")
    async def get_robot(robot_id: str):
        # récupération infos robot dans base
        return {"id": robot_id, "status": "active"}

### 7.3 Lancement serveur

    uvicorn main:app --reload

---

## 8. Console de Contrôle (Tkinter)

- Fenêtre principale affichant : 
  - Bouton et champ de texte permettant la connexion avec le robot voulu.
  - État robot (position, état pince, actions, distance ultrasons).
  - Boutons pour envoyer objectif (basée sur une logique commune à tout les groupes).  
  - Journaux des messages reçus.

---

## 9. Console de Simulation (Java)

- Fenêtre graphique représentant la zone de jeu.  
- Affichage du robot en position (x,y) avec orientation.  
- Mise à jour en temps réel selon commandes reçues.  
- Tests des algorithmes de contrôle.

---

## 10. Base de données SQLite

- Table robots (id UUID, nom, statut, position).  
- Table missions (id, robot_id, description, statut).  
- Enregistrement des logs et données historiques.

---

## 11. Documentation et Présentation

- Génération automatique avec Doxygen pour le code embarqué.  
- Auto-évaluation journalière.
- Rapport journalier sur les exploits de la journée ainsi que les futures missions.
- Diagramme de Gantt.
- Vidéo démonstration de la solution finale.
- Présentation orale de 15 minutes.

---

## 12. Problèmes connus et pistes d’amélioration

- Latence entre le moment où l'on capte la ligne et le moment où l'on envoie l'instruction de tourner.  
- Optimiser l'envoie d'énergie.  
- Ajout d'une carroserie plus complète pour le robot.  
- Interface web plus complète (statistiques graphiques).

---

## 13. Contacts et Ressources

- Référents : Mr. Madeline Blaise, Mr. Delcombel Pascal & Mme. Dolle-Fabre Cécile 
- Documentation MicroPython : https://docs.micropython.org  
- FastAPI : https://fastapi.tiangolo.com  
- SQLite : https://sqlite.org/index.html

---
