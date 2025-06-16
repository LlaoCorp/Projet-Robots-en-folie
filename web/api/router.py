import sys
import os
import ast

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import APIRouter, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pathlib import Path
from uuid import uuid4
from database.service import *
from database.base_model import Instruction, Initialisation, Telemetry, Summary, REF

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root():
    uuid = str(uuid4())
    print(uuid)
    with open('web/templates/index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@router.post("/create", response_class=HTMLResponse)
async def create(name: str = Form(...), id: str = Form(...)):
    success = create_robot(id, name)
    if success:
        return JSONResponse(content={"status": "success", "message": f"Robot '{name}' créé avec succès."}, status_code=200)
    return JSONResponse(content={"status": "error", "message": f"Le robot avec l'ID '{id}' existe déjà."}, status_code=200)

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
    success = enregistrer_instruction(instruction.robot_id, instruction.blocks, instruction.status)
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
        return {"success": True, "blocks": ast.literal_eval(instruction["blocks"])}
    return {"success": False, "message": "Aucune instruction en cours pour ce robot."}

@router.post("/instructions/change_status/{robot_id}")
async def changer_status_instruction_route(robot_id: str, request: Request):
    payload = await request.json()
    success = changer_status_instruction(robot_id, payload['status'])
    if success:
        return {"status": "Statut changé avec succès"}
    return {"status": "Erreur lors du changement de status"}

@router.post("/message")
async def message(request: Request):
    payload = await request.json()
    ajouter_message(payload['robot_id'], payload['message'])
    return {"status": "Message reçu avec succès"}

@router.get("/message/{robot_id}")
async def get_message(robot_id: str):
    messages = recuperer_messages(robot_id)
    if messages:
        return {"robot_id": robot_id, "messages": messages}
    return {"error": "Aucun message trouvé pour ce robot."}
