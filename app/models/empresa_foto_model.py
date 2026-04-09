from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class EmpresaFoto(Base):
    __tablename__ = "empresa_fotos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)

    empresa_id = Column(Integer, ForeignKey("empresas.id"))

    empresa = relationship(
        "Empresa",
        back_populates="fotos"
    )