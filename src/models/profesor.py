from .persona import Persona
from pydantic import Field

class Profesor(Persona):
    numeroEmpleado: int = Field(0)
    horasClase: int = Field(0)
    class Config:
        from_attributes = True
    