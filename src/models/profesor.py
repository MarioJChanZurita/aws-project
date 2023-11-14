from .person import Person
from pydantic import Field

class Profesor(Person):
    numeroEmpleado: str = Field(...)
    horasClase: int = Field(...)