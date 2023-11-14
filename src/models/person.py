from pydantic import BaseModel
from pydantic import Field

class Person(BaseModel):
    id: int = Field(...)
    nombres: str = Field(...)
    apellidos: str = Field(...)