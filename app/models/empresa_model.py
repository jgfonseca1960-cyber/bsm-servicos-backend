from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.associacoes import empresa_tipo_servico


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    telefone = Column(String, nullable=False)

    cnpj = Column(String, nullable=True)
    cpf = Column(String, nullable=True)

    endereco = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    estado = Column(String, nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    ativo = Column(Boolean, default=True)
    avaliacao_media = Column(Float, default=0)

    # =========================
    # RELACIONAMENTOS
    # =========================

    fotos = relationship(
        "EmpresaFoto",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )

    servicos = relationship(
    "Servico",
    back_populates="empresa",
    cascade="all, delete-orphan"
)

    # ✅ RELACIONAMENTO CORRETO MANY-TO-MANY
    tipos_servico = relationship(
        "TipoServico",
        secondary=empresa_tipo_servico,
        back_populates="empresas"
    )