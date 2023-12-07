from pydantic import BaseModel, Field
from typing import Optional


class Persona(BaseModel):
    id: Optional[int]
    nombres: str = Field(...)
    apellidos: str = Field(...)