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
    Column("servico_id", Integer, ForeignKey("servicos.id"), primary_key=True),
)
