from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# =========================
# TABELA DE ASSOCIAÇÃO (MANY-TO-MANY)
# =========================
empresa_servico = Table(
    "empresa_servico",
    Base.metadata,
    Column("empresa_id", Integer, ForeignKey("empresas.id"), primary_key=True),
    Column("servico_id", Integer, ForeignKey("servicos.id"), primary_key=True),  # 🔥 corrigido aqui
)

# =========================
# TABELA EMPRESAS
# =========================
class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String)
    endereco = Column(String)

    # relacionamento MANY-TO-MANY
    servicos = relationship(
        "Servico",
        secondary=empresa_servico,
        back_populates="empresas"
    )

# =========================
# TABELA SERVIÇOS
# =========================
class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    # relacionamento MANY-TO-MANY
    empresas = relationship(
        "Empresa",
        secondary=empresa_servico,
        back_populates="servicos"
    )