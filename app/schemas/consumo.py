from pydantic import BaseModel
from typing import Optional

class ConsumoBase(BaseModel):
    mes: str
    kwh_consumido: float
    costo_cop: float
    tarifa_cop_kwh: Optional[float] = 0.0

class ConsumoCreate(ConsumoBase):
    sede_id: int

class ConsumoResponse(ConsumoBase):
    id: int
    sede_id: int

    class Config:
        from_attributes = True

class ConsumoResumenSede(BaseModel):
    sede_id: int
    nombre_sede: str
    total_kwh: float
    total_costo_cop: float
    promedio_mensual_kwh: float
    promedio_mensual_cop: float
    tarifa_promedio_cop_kwh: float