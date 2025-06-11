from pydantic import BaseModel
from datetime import datetime

class EtatRobot(BaseModel):
    ref_id: str
    position: int
    has_box: bool
    objectif: str

class ActionRobot(BaseModel):
    ref_id: str
    action: str
    position: int

class Mission(BaseModel):
    ref_id: str
    num_cube: str
    statut: str
class Initialisation(BaseModel):
    ref_id: str
    position: int
    has_box: bool
class Message(BaseModel):
    ref_id: str
    contenu: str

class REF(BaseModel):
    ref_id: str