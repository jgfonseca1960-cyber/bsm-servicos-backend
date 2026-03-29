from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    tipo_id = Column(Integer, ForeignKey("tipos_servico.id"))

    tipo = relationship("TipoServico")