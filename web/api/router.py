import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uvicorn
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from uuid import uuid4
from database.service import *
from database.base_model import Instruction, Message, EtatRobot, ActionRobot, Initialisation, Telemetry, Summary

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

@router.post("/envoyer")
async def envoyer_message(msg: Message):
    print(f"📩 Message reçu de {msg.ref_id} : {msg.contenu}")
    ajouter_message(msg.ref_id, msg.contenu)
    return {"status": "ok", "message": msg.contenu}

@router.get("/messages")
async def get_messages():
    return recuperer_messages()

@router.get("/missions/{ref_id}")
async def list_missions(ref_id: str):
    missions = get_missions(ref_id)
    if missions:
        return {"ref_id": ref_id, "missions": missions}
    return {"error": "Aucune mission trouvée pour ce robot."}

@router.post("/etat")
async def recevoir_etat(etat: EtatRobot):
    enregistrer_etat_robot(etat)
    return {"status": "etat reçu"}

@router.get("/etats/{ref_id}")
async def get_etat(ref_id: str):
    etats = get_etats(ref_id)
    if etats:
        return {"ref_id": ref_id, "etats": etats}
    return {"error": "Aucune mission trouvée pour ce robot."}

@router.post("/action")
async def enregistrer_action(action: ActionRobot):
    ajouter_action_en_base(action)
    return {"status": "action enregistrée"}

@router.get("/actions/{ref_id}")
async def get_action(ref_id: str):
    actions = get_actions(ref_id)
    if actions:
        return {"ref_id": ref_id, "actions": actions}
    return {"error": "Aucune mission trouvée pour ce robot."}

@router.post("/initialiser")
async def initialiser_robot(data: Initialisation):
    enregistrer_robot(data)
    return {"status": "robot initialisé"}

@router.post("/telemetry")
async def telemetry(telemetry: Telemetry):
    enregistrer_telemetry(telemetry)
    return {"status": "télémetrie reçue"}

@router.post("/summary")
async def summary(summary: Summary):
    enregistrer_summary(summary)
    return {"status": "résumé reçu"}

@router.post("/instructions")
async def recevoir_instruction(instruction: Instruction):
    enregistrer_instruction(instruction.robot_id, instruction.blocks, instruction.statut)
    return {"status": "instruction enregistrée"}

@router.get("/instructions/{robot_id}")
async def recuperer_instruction(robot_id: str):
    instruction = get_current_instruction(robot_id)
    if instruction:
        return instruction
    return {"error": "Aucune instruction en cours pour ce robot."}

@router.post("/instructions/change_statut/{robot_id}")
async def changer_statut_instruction_route(robot_id: str, request: Request):
    payload = await request.json()
    statut = payload.get("statut")
    if not statut:
        return {"error": "Champ 'statut' manquant"}
    success = changer_statut_instruction(robot_id, statut)
    return {"status": "ok" if success else "erreur", "statut": statut}

@router.post("/summary")
async def summary(data: Initialisation):
    enregistrer_robot(data)
    return {"status": "résumé reçu"}

