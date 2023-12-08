from .persona import Persona
from pydantic import Field

class Alumno(Persona):
    matricula: str = Field('')
    promedio: float = Field(0.0)
    fotoPerfilUrl: str | None = None
    password: str = Field('')
    class Config:
        from_attributes = True
    