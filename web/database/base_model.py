from pydantic import BaseModel

class Initialisation(BaseModel):
    ref_id: str
    position: int
    has_box: bool

class Message(BaseModel):
    ref_id: str
    contenu: str

class REF(BaseModel):
    name: str
    id: str

class Telemetry(BaseModel):
    robot_id: str = None
    vitesse_instant: float = None
    ds_ultrasons: float = None
    statut_deplacement: str = None
    ligne: int = None
    statut_pince: bool = None

class Summary(BaseModel):
    robot_id: str = None

class Instruction(BaseModel):
    robot_id: str
    blocks: list[int]
    status: str

