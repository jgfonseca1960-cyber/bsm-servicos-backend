from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    empresa_id = Column(Integer, ForeignKey("empresas.id"))
    tipo_servico_id = Column(Integer, ForeignKey("tipos_servico.id"))

    # Relacionamentos
    empresa = relationship("Empresa", back_populates="servicos")
    tipo_servico = relationship("TipoServico")