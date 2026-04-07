from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.tipo_servico_model import TipoServico


class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    # 🔗 ligação com empresa
    empresa_id = Column(Integer, ForeignKey("empresas.id"))

    # 🔗 ligação com tipo de serviço
    tipo_id = Column(Integer, ForeignKey("tipos_servico.id"))

    # relacionamentos
    empresa = relationship("Empresa", back_populates="servicos")
    tipo = relationship("TipoServico")