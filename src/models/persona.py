from pydantic import BaseModel, Field
from typing import Optional


class Persona(BaseModel):
    id: Optional[int] = None
    nombres: str = Field('')
    apellidos: str = Field('')
    class Config:
        from_attributes = True