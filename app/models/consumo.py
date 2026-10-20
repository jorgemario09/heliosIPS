from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ConsumoHistorico(Base):
    __tablename__ = "consumo_historico"

    id = Column(Integer, primary_key=True, index=True)
    sede_id = Column(Integer, ForeignKey("sedes_ips.id", ondelete="CASCADE"), nullable=False, index=True)
    mes = Column(String(30), nullable=False, index=True)
    kwh_consumido = Column(Numeric(12, 2), nullable=False, default=0.00)
    costo_cop = Column(Numeric(15, 2), nullable=False, default=0.00)
    tarifa_cop_kwh = Column(Numeric(10, 2), default=0.00)

    sede = relationship("SedeIPS", back_populates="consumos")