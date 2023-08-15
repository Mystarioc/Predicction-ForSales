from pydantic import BaseModel
from datetime import date
from typing import List

class FechasInput(BaseModel):
    fechaInicio: date
    fechaFin: date
    Namedb: str

class CredencialesDatosEntrenamiento(BaseModel):
    Namedb: str
    usuario:str
    contra: str
