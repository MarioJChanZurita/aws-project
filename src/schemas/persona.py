from sqlalchemy import Column, Integer, String
from src.utils.MySQL import Base

class Persona(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)