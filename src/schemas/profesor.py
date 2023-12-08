from sqlalchemy import Column, Integer, String
from src.utils.database import Base

class Profesor(Base):
    __tablename__ = 'profesores'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)

    numeroEmpleado = Column(Integer, unique=True, nullable=False)
    horasClase = Column(Integer)