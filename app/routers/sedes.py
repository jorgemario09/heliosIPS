from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.sede import SedeIPS
from app.models.consumo import ConsumoHistorico
from app.schemas.sede import SedeResponse, SedeCreate

router = APIRouter(prefix="/sedes", tags=["Sedes IPS"])

@router.get("/", response_model=List[SedeResponse])
def listar_sedes(db: Session = Depends(get_db)):
    # Filtra y retorna únicamente las sedes que tienen al menos un registro en consumo_historico
    return db.query(SedeIPS)\
        .join(ConsumoHistorico, SedeIPS.id == ConsumoHistorico.sede_id)\
        .distinct()\
        .order_by(SedeIPS.nombre)\
        .all()

@router.get("/{sede_id}", response_model=SedeResponse)
def obtener_sede(sede_id: int, db: Session = Depends(get_db)):
    sede = db.query(SedeIPS).filter(SedeIPS.id == sede_id).first()
    if not sede:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sede IPS no encontrada"
        )
    return sede

@router.post("/", response_model=SedeResponse, status_code=status.HTTP_201_CREATED)
def crear_sede(sede_in: SedeCreate, db: Session = Depends(get_db)):
    existing = db.query(SedeIPS).filter(SedeIPS.nombre == sede_in.nombre).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una sede con este nombre"
        )
    
    db_sede = SedeIPS(**sede_in.model_dump())
    db.add(db_sede)
    db.commit()
    db.refresh(db_sede)
    return db_sede