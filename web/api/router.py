import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uvicorn
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from uuid import uuid4
from database.service import *
from database.base_model import Message, EtatRobot, ActionRobot, Initialisation

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h2>Console REF</h2>
    <form action="/create" method="post">
        <input type="text" name="name" placeholder="Nom du robot" required>
        <button type="submit">Créer un robot</button>
    </form>
    <br>
    <a href="/missions">Voir les missions</a>
    """

@router.post("/create", response_class=HTMLResponse)
async def create(name: str = Form(...)):
    uuid = create_robot(name)
    return f"Robot '{name}' créé avec UUID : {uuid}<br><a href='/'>Retour</a>"

@router.get("/mission/{ref_id}")
async def get_mission(ref_id: str):
    missions = get_mission(ref_id)
    if missions:
        return {"ref_id": ref_id, "missions": missions}
    return {"error": "Aucune mission trouvée pour ce robot."}


@router.get("/missions", response_class=HTMLResponse)
async def missions():
    mission_data = list_missions()
    html = "<h3>Missions</h3><ul>"
    for m in mission_data:
        html += f"<li>{m}</li>"
    html += "</ul><a href='/'>Retour</a>"
    return html

@router.post("/envoyer/")
async def envoyer_message(msg: Message):
    ajouter_message(msg.ref_id, msg.contenu)
    return {"status": "ok", "message": msg.contenu}

@router.get("/messages/")
async def get_messages():
    return recuperer_messages()

@router.post("/etat/")
async def recevoir_etat(etat: EtatRobot):
    enregistrer_etat_robot(etat)
    return {"status": "etat reçu"}

@router.get("/etats/{ref_id}")
async def get_etat(ref_id: str):
    etats = get_etats(ref_id)
    if etats:
        return {"ref_id": ref_id, "etats": etats}
    return {"error": "Aucune mission trouvée pour ce robot."}

@router.post("/action/")
async def enregistrer_action(action: ActionRobot):
    ajouter_action_en_base(action)
    return {"status": "action enregistrée"}

@router.get("/actions/{ref_id}")
async def get_action(ref_id: str):
    actions = get_actions(ref_id)
    if actions:
        return {"ref_id": ref_id, "actions": actions}
    return {"error": "Aucune mission trouvée pour ce robot."}

@router.post("/initialiser/")
async def initialiser_robot(data: Initialisation):
    enregistrer_robot(data)
    return {"status": "robot initialisé"}