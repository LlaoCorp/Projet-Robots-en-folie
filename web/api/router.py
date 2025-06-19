## @file router.py
#  @brief Définition des routes de l’API REST pour le simulateur de robot.
#  Gère les requêtes entrantes (création de robot, instructions, télémétrie, messages...).

import sys
import os
import ast

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import APIRouter, Form, Request, Query
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pathlib import Path
from database.service import *
from database.base_model import Instruction, Initialisation, Telemetry, Summary, REF

router = APIRouter()

## @brief Page d’accueil HTML du serveur avec formulaires de test.
#  @return HTML avec interface utilisateur.
@router.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html lang=\"fr\">
    <head>
        <meta charset=\"UTF-8\">
        <title>Console REF - Interface Serveur</title>
        <link rel=\"stylesheet\" href=\"../static/styles.css\">
    </head>
    <body>
        <div class=\"container\">
            <h1>Console REF - Interface Serveur</h1>

            <section>
                <h2>Créer un nouveau robot</h2>
                <form method=\"post\" action=\"/create\">
                    <input type=\"text\" name=\"name\" placeholder=\"Nom du robot\" required>
                    <input type=\"text\" name=\"id\" placeholder=\"ID du robot\" required>
                    <button type=\"submit\">Créer</button>
                </form>
            </section>

            <section>
                <h2>Consulter les missions</h2>
                <form method=\"get\" action=\"/missions\">
                    <input type=\"text\" name=\"robot_id\" placeholder=\"ID du robot\" required>
                    <button type=\"submit\">Voir missions</button>
                </form>
            </section>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

## @brief Création d’un nouveau robot dans la base de données via formulaire HTML.
#  @param name Nom du robot.
#  @param id Identifiant unique du robot.
#  @return HTML confirmant la création ou l’échec.
@router.post("/create", response_class=HTMLResponse)
async def create(name: str = Form(...), id: str = Form(...)):
    success = create_robot(id, name)
    message = f"Robot '{name}' créé avec succès." if success else f"Le robot avec l'ID '{id}' existe déjà."
    html = f"""
    <!DOCTYPE html>
    <html lang=\"fr\">
    <head>
        <meta charset=\"UTF-8\">
        <title>Confirmation création robot</title>
        <link rel=\"stylesheet\" href=\"../static/styles.css\">
    </head>
    <body>
        <div class=\"container\">
            <h1>{message}</h1>
            <a href=\"/\">Retour à l'accueil</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

## @brief Affiche les instructions (missions) d’un robot spécifique.
#  @param robot_id ID du robot ciblé.
#  @return HTML avec la liste des missions ou message d’erreur.
@router.get("/missions", response_class=HTMLResponse)
async def consulter_missions(robot_id: str = Query(...)):
    instructions = get_instructions(robot_id)
    bloc_html = ""

    if instructions:
        for instruction in instructions:
            bloc_html += f"""
            <div class=\"instruction-card\">
                <h3>Mission</h3>
                <div><strong>Blocs à récupérer :</strong> {instruction['blocks']}</div>
            </div>
            """
    else:
        bloc_html = "<p>Aucune instruction trouvée pour ce robot.</p>"

    html = f"""
    <!DOCTYPE html>
    <html lang=\"fr\">
    <head>
        <meta charset=\"UTF-8\">
        <title>Missions du robot</title>
        <link rel=\"stylesheet\" href=\"../static/styles.css\">
    </head>
    <body>
        <div class=\"container\">
            <h1>Missions du robot {robot_id}</h1>
            {bloc_html}
            <a href=\"/\">Retour à l'accueil</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

## @brief Reçoit des données de télémétrie pour un robot.
#  @param telemetry Objet contenant les données de télémétrie.
#  @return Statut de réception.
@router.post("/telemetry")
async def telemetry(telemetry: Telemetry):
    enregistrer_telemetry(telemetry)
    return {"status": "télémétrie reçue"}

## @brief Récupère les dernières données de télémétrie pour un robot.
#  @param robot_id Identifiant du robot.
#  @return Données télémétriques ou message d’erreur.
@router.get("/telemetry/{robot_id}")
async def get_telemetry(robot_id: str):
    telemetry = recuperer_telemetry(robot_id)
    if telemetry:
        return telemetry
    return {"error": "Aucune télémétrie trouvée pour ce robot."}

## @brief Reçoit le résumé d'une mission.
#  @param summary Objet contenant le résumé de mission.
#  @return Statut de réception.
@router.post("/summary")
async def summary(summary: Summary):
    enregistrer_summary(summary)
    return {"status": "résumé reçu"}

## @brief Enregistre une nouvelle instruction pour un robot.
#  @param instruction Objet instruction contenant les blocs et le statut.
#  @return Statut de l'opération.
@router.post("/instructions")
async def recevoir_instruction(instruction: Instruction):
    success = enregistrer_instruction(instruction.robot_id, instruction.blocks, instruction.status)
    if success :
        return {"status": "Instruction enregistrée"}
    return {"status": "Robot non trouvé"}

## @brief Liste toutes les instructions d'un robot.
#  @param robot_id Identifiant du robot.
#  @return Liste d'instructions.
@router.get("/list-instructions/{robot_id}")
async def list_missions(robot_id: str):
    instructions = get_instructions(robot_id)
    if instructions:
        return {"robot_id": robot_id, "instructions": instructions}
    return {"error": "Aucune instruction en cours pour ce robot."}

## @brief Récupère la dernière instruction en cours d'un robot.
#  @param robot_id Identifiant du robot.
#  @return Blocs de l'instruction en cours.
@router.get("/instructions")
async def recuperer_instruction(robot_id: str):
    instruction = get_current_instruction(robot_id)
    if instruction:
        return {"success": True, "blocks": ast.literal_eval(instruction["blocks"])}
    return {"success": False, "message": "Aucune instruction en cours pour ce robot."}

## @brief Change le statut de la dernière instruction d'un robot.
#  @param robot_id Identifiant du robot.
#  @param request Corps de la requête contenant le nouveau statut.
#  @return Statut de l'opération.
@router.post("/instructions/change_status/{robot_id}")
async def changer_status_instruction_route(robot_id: str, request: Request):
    payload = await request.json()
    success = changer_status_instruction(robot_id, payload['status'])
    if success:
        return {"status": "Statut changé avec succès"}
    return {"status": "Erreur lors du changement de status"}

##
# @brief Reçoit un message pour un robot (utilisé pour les tests uniquement).
@router.post("/message")
async def message(request: Request):
    payload = await request.json()
    ajouter_message(payload['robot_id'], payload['message'])
    return {"status": "Message reçu avec succès"}

##
# @brief Récupère tous les messages enregistrés (utilisé pour les tests).
@router.get("/messages")
async def get_message():
    messages = recuperer_messages()
    if messages:
        return {"messages": messages}
    return {"error": "Aucun message trouvé pour ce robot."}

## @brief Récupère les temps de mission d’un robot.
#  @param robot_id Identifiant du robot.
#  @return Liste de durées ou message d’erreur.
@router.get("/stats/{robot_id}")
async def get_stats(robot_id: str):
    temps_missions = recuperer_temps_missions(robot_id)
    if temps_missions:
        return {"success": True, "temps_missions": temps_missions}
    return {"success": False, "message": "Aucune donnée de mission trouvée."}
