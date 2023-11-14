from pydantic import BaseModel
from pydantic import Field

class Persona(BaseModel):
    id: int = Field(...)
    nombres: str = Field(...)
    apellidos: str = Field(...)