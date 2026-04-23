from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class EmpresaFoto(Base):
    __tablename__ = "empresa_fotos"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"))

    url = Column(String, nullable=False)

    # ✅ NOVO CAMPO
    principal = Column(Boolean, default=False)

    empresa = relationship("Empresa", back_populates="fotos")