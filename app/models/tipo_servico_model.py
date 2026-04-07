from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class TipoServico(Base):
    __tablename__ = "tipos_servico"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    empresas = relationship(
        "Empresa",
        secondary="empresa_tipo_servico",
        back_populates="tipos_servico"
    )

    from app.models.associacoes import empresa_tipo_servico

    empresas = relationship(
        "Empresa",
        secondary=empresa_tipo_servico,
        back_populates="tipos_servico"
    )

    empresa = relationship("Empresa", back_populates="tipos_servico")
