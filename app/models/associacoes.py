from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

empresa_tipo_servico = Table(
    "empresa_tipo_servico",
    Base.metadata,
    Column("empresa_id", Integer, ForeignKey("empresas.id"), primary_key=True),
    Column("tipo_servico_id", Integer, ForeignKey("tipos_servico.id"), primary_key=True),
)