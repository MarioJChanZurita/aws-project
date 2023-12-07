from .persona import Persona
from sqlalchemy import Column, String, Float

class Alumno(Persona):
    __tablename__ = 'alumnos'

    matricula = Column(String(10), nullable=False)
    promedio = Column(Float, nullable=False)
    fotoPerfilUrl = Column(String(100))
    password = Column(String(50), nullable=False)