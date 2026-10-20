from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class SedeIPS(Base):
    __tablename__ = "sedes_ips"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False, unique=True, index=True)
    direccion = Column(String(250))
    nic = Column(String(50))
    ciudad = Column(String(50), default="Barranquilla")

    consumos = relationship("ConsumoHistorico", back_populates="sede", cascade="all, delete-orphan")
    simulaciones = relationship("DimensionamientoSolar", back_populates="sede", cascade="all, delete-orphan")