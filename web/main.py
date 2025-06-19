"""
@file main.py
@brief Point d'entrée de l'application FastAPI pour la gestion des robots.

Ce fichier configure et démarre le serveur FastAPI,
monte les fichiers statiques, gère les routes API, autorise les origines CORS
et initialise la base de données si exécuté directement.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.router import router as robot_router
from fastapi.middleware.cors import CORSMiddleware
from database.init_db import init_db
from pathlib import Path

# Répertoire de base du projet
BASE_DIR = Path(__file__).resolve().parent

# Création de l'application FastAPI
app = FastAPI()

# Montage des fichiers statiques pour l'accès aux ressources
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Liste des origines autorisées pour les requêtes CORS
origins = [
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://localhost:8000",
    "http://0.0.0.0:8000",
    "http://10.7.5.148",
    "http://10.7.5.131",
    "http://192.168.1.21",
]

# Middleware CORS pour autoriser les échanges inter-domaines
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion du routeur contenant les endpoints pour la gestion des robots
app.include_router(robot_router)

# Lancement du serveur en mode développement si exécuté directement
if __name__ == "__main__":
    init_db()  # Initialisation de la base de données
    import uvicorn
    uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")
