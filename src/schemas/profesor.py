from .persona import Persona
from sqlalchemy import Column, Integer


class Profesor(Persona):
    __tablename__ = 'profesores'

    numeroEmpleado = Column(Integer, unique=True, nullable=False)
    horasClase = Column(Integer)