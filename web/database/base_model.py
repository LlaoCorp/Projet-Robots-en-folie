from pydantic import BaseModel

class Message(BaseModel):
    ref_id: str
    contenu: str

class REF(BaseModel):
    ref_id: str,