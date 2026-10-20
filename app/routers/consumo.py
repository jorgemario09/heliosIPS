from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.sede import SedeIPS
from app.models.consumo import ConsumoHistorico
from app.schemas.consumo import ConsumoResponse, ConsumoResumenSede

router = APIRouter(prefix="/consumo", tags=["Consumo Energético"])

@router.get("/sede/{sede_id}", response_model=List[ConsumoResponse])
def obtener_consumo_por_sede(sede_id: int, db: Session = Depends(get_db)):
    sede = db.query(SedeIPS).filter(SedeIPS.id == sede_id).first()
    if not sede:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sede IPS no encontrada"
        )
    return db.query(ConsumoHistorico).filter(ConsumoHistorico.sede_id == sede_id).all()

@router.get("/sede/{sede_id}/resumen", response_model=ConsumoResumenSede)
def obtener_resumen_consumo_sede(sede_id: int, db: Session = Depends(get_db)):
    sede = db.query(SedeIPS).filter(SedeIPS.id == sede_id).first()
    if not sede:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sede IPS no encontrada"
        )
    
    consumos = db.query(ConsumoHistorico).filter(ConsumoHistorico.sede_id == sede_id).all()
    if not consumos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La sede no registra consumos históricos"
        )
    
    total_kwh = sum(float(c.kwh_consumido) for c in consumos)
    total_costo = sum(float(c.costo_cop) for c in consumos)
    num_meses = len(consumos)
    prom_kwh = total_kwh / num_meses if num_meses > 0 else 0
    prom_costo = total_costo / num_meses if num_meses > 0 else 0
    tarifa_prom = total_costo / total_kwh if total_kwh > 0 else 0

    return ConsumoResumenSede(
        sede_id=sede.id,
        nombre_sede=sede.nombre,
        total_kwh=round(total_kwh, 2),
        total_costo_cop=round(total_costo, 2),
        promedio_mensual_kwh=round(prom_kwh, 2),
        promedio_mensual_cop=round(prom_costo, 2),
        tarifa_promedio_cop_kwh=round(tarifa_prom, 2)
    )