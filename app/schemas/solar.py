from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DimensionarRequest(BaseModel):
    sede_id: int = Field(..., description="ID de la sede IPS")
    cobertura_pct: float = Field(..., ge=0.01, le=1.0, description="Cobertura entre 0.01 (1%) y 1.0 (100%)")
    hsp: Optional[float] = Field(default=5.2, ge=1.0, le=10.0)
    pr: Optional[float] = Field(default=0.80, ge=0.1, le=1.0)
    potencia_panel_w: Optional[int] = Field(default=550, ge=100, le=1000)

class DimensionarResponse(BaseModel):
    id: Optional[int] = None
    sede_id: int
    nombre_sede: str
    cobertura_porcentaje: float
    kwp_requerido: float
    cantidad_paneles_550w: int
    area_requerida_m2: float
    ahorro_mensual_cop: float
    ahorro_anual_cop: float
    capex_estimado_cop: float
    payback_anos: float
    co2_evitado_ton_ano: float
    fecha_calculo: Optional[datetime] = None

    class Config:
        from_attributes = True