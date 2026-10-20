import math
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.sede import SedeIPS
from app.models.consumo import ConsumoHistorico
from app.models.solar import DimensionamientoSolar
from app.schemas.solar import DimensionarRequest, DimensionarResponse

router = APIRouter(prefix="/solar", tags=["Dimensionamiento Solar"])

@router.post("/dimensionar", response_model=DimensionarResponse, status_code=status.HTTP_201_CREATED)
def calcular_y_guardar_dimensionamiento(req: DimensionarRequest, db: Session = Depends(get_db)):
    sede = db.query(SedeIPS).filter(SedeIPS.id == req.sede_id).first()
    if not sede:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sede IPS no encontrada"
        )

    consumos = db.query(ConsumoHistorico).filter(ConsumoHistorico.sede_id == req.sede_id).all()
    if not consumos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La sede no cuenta con registros históricos de consumo"
        )

    total_kwh = sum(float(c.kwh_consumido) for c in consumos)
    total_cop = sum(float(c.costo_cop) for c in consumos)
    num_meses = len(consumos)

    kwh_promedio_mes = total_kwh / num_meses
    costo_promedio_mes = total_cop / num_meses

    # Algoritmo de Cálculo Fotovoltaico
    kwh_dia = kwh_promedio_mes / 30.0
    kwh_solar_dia = kwh_dia * req.cobertura_pct

    kwp_requerido = kwh_solar_dia / (req.hsp * req.pr)
    num_paneles = math.ceil((kwp_requerido * 1000) / req.potencia_panel_w)
    
    # Inversores trifásicos On-Grid de 50 kW sugeridos para la potencia calculada
    inversores_50kw = math.ceil(kwp_requerido / 50.0) if kwp_requerido > 0 else 1
    area_m2 = num_paneles * 2.2

    ahorro_mensual_cop = costo_promedio_mes * req.cobertura_pct
    ahorro_anual_cop = ahorro_mensual_cop * 12.0
    
    # CAPEX (Gastos de Capital) Llave en Mano: $3.8M COP/kWp (Paneles + Inversores + Cableado + Estructura + Mano de obra)
    capex_estimado_cop = kwp_requerido * 3800000.0
    payback_anos = capex_estimado_cop / ahorro_anual_cop if ahorro_anual_cop > 0 else 0
    co2_evitado_ton = ((kwh_promedio_mes * 12 * req.cobertura_pct) * 0.35) / 1000.0

    nueva_simulacion = DimensionamientoSolar(
        sede_id=req.sede_id,
        porcentaje_cobertura=req.cobertura_pct * 100,
        kwp_requerido=round(kwp_requerido, 2),
        cantidad_paneles=num_paneles,
        area_m2=round(area_m2, 2),
        ahorro_mensual_cop=round(ahorro_mensual_cop, 2),
        ahorro_anual_cop=round(ahorro_anual_cop, 2),
        capex_estimado_cop=round(capex_estimado_cop, 2),
        payback_anos=round(payback_anos, 1),
        co2_evitado_ton_ano=round(co2_evitado_ton, 2)
    )

    db.add(nueva_simulacion)
    db.commit()
    db.refresh(nueva_simulacion)

    return DimensionarResponse(
        id=nueva_simulacion.id,
        sede_id=sede.id,
        nombre_sede=sede.nombre,
        cobertura_porcentaje=req.cobertura_pct * 100,
        kwp_requerido=round(kwp_requerido, 2),
        cantidad_paneles_550w=num_paneles,
        inversores_50kw_estimados=inversores_50kw,
        tipo_sistema="On-Grid (Sin Baterías)",
        descripcion_bos="Cableado DC/AC + Estructuras + Protecciones",
        area_requerida_m2=round(area_m2, 2),
        ahorro_mensual_cop=round(ahorro_mensual_cop, 2),
        ahorro_anual_cop=round(ahorro_anual_cop, 2),
        capex_estimado_cop=round(capex_estimado_cop, 2),
        payback_anos=round(payback_anos, 1),
        co2_evitado_ton_ano=round(co2_evitado_ton, 2),
        fecha_calculo=nueva_simulacion.fecha_calculo
    )