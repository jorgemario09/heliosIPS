from sqlalchemy import Column, Integer, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class DimensionamientoSolar(Base):
    __tablename__ = "dimensionamiento_solar"

    id = Column(Integer, primary_key=True, index=True)
    sede_id = Column(Integer, ForeignKey("sedes_ips.id", ondelete="CASCADE"), nullable=False, index=True)
    porcentaje_cobertura = Column(Numeric(5, 2), nullable=False)
    kwp_requerido = Column(Numeric(10, 2), nullable=False)
    cantidad_paneles = Column(Integer, nullable=False)
    area_m2 = Column(Numeric(10, 2))
    ahorro_mensual_cop = Column(Numeric(15, 2))
    ahorro_anual_cop = Column(Numeric(15, 2))
    capex_estimado_cop = Column(Numeric(15, 2))
    payback_anos = Column(Numeric(5, 2))
    co2_evitado_ton_ano = Column(Numeric(10, 2))
    fecha_calculo = Column(DateTime(timezone=True), server_default=func.now())

    sede = relationship("SedeIPS", back_populates="simulaciones")