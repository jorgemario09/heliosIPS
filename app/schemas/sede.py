from pydantic import BaseModel
from typing import Optional

class SedeBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    nic: Optional[str] = None
    ciudad: Optional[str] = "Barranquilla"

class SedeCreate(SedeBase):
    pass

class SedeResponse(SedeBase):
    id: int

    class Config:
        from_attributes = True