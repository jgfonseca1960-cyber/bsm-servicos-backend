from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database import Base

class Empresa(Base):

    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)

    descricao = Column(String)

    telefone = Column(String)
    whatsapp = Column(String)
    email = Column(String)

    endereco = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    estado = Column(String)
    cep = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)

    ativo = Column(Boolean, default=True)

    cpf = Column(String)
    cnpj = Column(String)



# =====================================================
# 🏆 PLANOS E DESTAQUES
# =====================================================
    
    destaque = Column(Boolean, default=False)

    plano = Column(String, default="gratuito")

    prioridade = Column(Integer, default=0)

    whatsapp_destacado = Column(
        Boolean,
        default=False
    )

    exibir_no_topo = Column(
        Boolean,
        default=False
    )

    selo_premium = Column(
        Boolean,
        default=False
    )

    # =====================================================
    # FK
    # =====================================================

    servico_id = Column(
        Integer,
        ForeignKey("servicos.id"),
        nullable=True
    )

    servico = relationship(
    "Servico",
    back_populates="empresas"
    )

    # =====================================================
    # RELACIONAMENTOS
    # =====================================================

    fotos = relationship(
        "EmpresaFoto",
        back_populates="empresa",
        cascade="all, delete"
    )

    avaliacoes = relationship(
        "Avaliacao",
        back_populates="empresa",
        cascade="all, delete"
    )