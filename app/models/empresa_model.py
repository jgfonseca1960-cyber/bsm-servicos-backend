from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.core.database import Base
# from app.db.base import Base


class Empresa(Base):

    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String)

    responsavel = Column(String)

    telefone = Column(String)

    endereco = Column(String)

    cidade = Column(String)

    estado = Column(String)

    tipo_servico = Column(String)

    descricao = Column(String)

    categoria = Column(String)

    latitude = Column(Float)

    longitude = Column(Float)

    usuarios = relationship(
        "Usuario",
        back_populates="empresa"
    )