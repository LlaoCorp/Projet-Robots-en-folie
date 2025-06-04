import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uvicorn
from fastapi import FastAPI
from uuid import uuid4
from gestion import enregistrer_message, lire_messages
from database.base_model import Message

app = FastAPI()

@app.post("/envoyer/")
async def envoyer_message(msg: Message):
    enregistrer_message(msg)
    return {"status": "ok", "message": msg.contenu}

@app.get("/messages/")
async def get_messages():
    return lire_messages()

# @app.post("/create_ref/")
# async def create_ref():
#     ref_id = str(uuid4())
#     return {"ref_id": ref_id}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
