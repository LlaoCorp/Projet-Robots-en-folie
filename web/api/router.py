import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uvicorn
from fastapi import APIRouter, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pathlib import Path
from uuid import uuid4
from database.service import *
from database.base_model import Instruction, Initialisation, Telemetry, Summary, REF

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root():
    with open('web/templates/index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@router.post("/create", response_class=HTMLResponse)
async def create(name: str = Form(...), id: str = Form(...)):
    success = create_robot(id, name)
    if success:
        return JSONResponse(content={"status": "success", "message": f"Robot '{name}' créé avec succès."}, status_code=200)
    return JSONResponse(content={"status": "error", "message": f"Le robot avec l'ID '{id}' existe déjà."}, status_code=200)

# @router.post("/envoyer")
# async def envoyer_message(msg: Message):
#     print(f"📩 Message reçu de {msg.ref_id} : {msg.contenu}")
#     ajouter_message(msg.ref_id, msg.contenu)
#     return {"status": "ok", "message": msg.contenu}

# @router.get("/messages")
# async def get_messages():
#     return recuperer_messages()

# @router.get("/missions/{ref_id}")
# async def list_missions(ref_id: str):
#     missions = get_missions(ref_id)
#     if missions:
#         return {"ref_id": ref_id, "missions": missions}
#     return {"error": "Aucune mission trouvée pour ce robot."}

# @router.post("/etat")
# async def recevoir_etat(etat: EtatRobot):
#     enregistrer_etat_robot(etat)
#     return {"status": "etat reçu"}

# @router.get("/etats/{ref_id}")
# async def get_etat(ref_id: str):
#     etats = get_etats(ref_id)
#     if etats:
#         return {"ref_id": ref_id, "etats": etats}
#     return {"error": "Aucune mission trouvée pour ce robot."}

# @router.post("/action")
# async def enregistrer_action(action: ActionRobot):
#     ajouter_action_en_base(action)
#     return {"status": "action enregistrée"}

# @router.get("/actions/{ref_id}")
# async def get_action(ref_id: str):
#     actions = get_actions(ref_id)
#     if actions:
#         return {"ref_id": ref_id, "actions": actions}
#     return {"error": "Aucune mission trouvée pour ce robot."}

# @router.post("/initialiser")
# async def initialiser_robot(data: Initialisation):
#     enregistrer_robot(data)
#     return {"status": "robot initialisé"}

@router.post("/telemetry")
async def telemetry(telemetry: Telemetry):
    print('ici : ', telemetry)
    enregistrer_telemetry(telemetry)
    return {"status": "télémetrie reçue"}

@router.get("/telemetry/{robot_id}")
async def get_telemetry(robot_id: str):
    telemetry = recuperer_telemetry(robot_id)
    if telemetry:
        return telemetry
    return {"error": "Aucune télémétrie trouvée pour ce robot."}

@router.post("/summary")
async def summary(summary: Summary):
    enregistrer_summary(summary)
    return {"status": "résumé reçu"}

@router.post("/instructions")
async def recevoir_instruction(instruction: Instruction):
    success = enregistrer_instruction(instruction.robot_id, instruction.blocks, instruction.statut)
    if success :
        return {"status": "Instruction enregistrée"}
    return {"status": "Robot non trouvé"}
        

@router.get("/list-instructions/{robot_id}")
async def list_missions(robot_id: str):
    instructions = get_instructions(robot_id)
    if instructions:
        return {"robot_id": robot_id, "instructions": instructions}
    return {"error": "Aucune instruction en cours pour ce robot."}

@router.get("/instructions/{robot_id}")
async def recuperer_instruction(robot_id: str):
    instruction = get_current_instruction(robot_id)
    if instruction:
        return {"success": True, "blocks": instruction["blocks"]}
    return {"success": False, "message": "Aucune instruction en cours pour ce robot."}

@router.post("/instructions/change_statut/{robot_id}")
async def changer_statut_instruction_route(robot_id: str, request: Request):
    payload = await request.json()
    statut = payload.get("statut")
    if not statut:
        return {"error": "Champ 'statut' manquant"}
    success = changer_statut_instruction(robot_id, statut)
    return {"status": "ok" if success else "erreur", "statut": statut}

@router.post("/summary")
async def summary(summary: Summary):
    enregistrer_robot(summary)
    return {"status": "résumé reçu"}

