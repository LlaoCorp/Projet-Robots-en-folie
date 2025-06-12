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

class Telemetry(BaseModel):
    robot_id: str = None
    vitesse_instant: float = None
    ds_ultrasons: float = None
    status_deplacement: str = None
    ligne: int = None
    status_pince: bool = None

class Summary(BaseModel):
    robot_id: str = None
    vitesse_moy: float = None

class Instruction(BaseModel):
    robot_id: str
    blocks: list[int]
    statut: str

