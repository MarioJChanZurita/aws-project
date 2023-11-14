from .persona import Persona
from pydantic import Field

class Profesor(Persona):
    numeroEmpleado: str = Field(...)
    horasClase: int = Field(...)