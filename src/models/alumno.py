from .persona import Persona

class Alumno(Persona):
    matricula: str
    promedio: float
    fotoPerfilUrl: str | None
    password: str