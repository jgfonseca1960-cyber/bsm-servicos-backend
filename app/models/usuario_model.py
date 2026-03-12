from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# from app.db.base import Base
from app.database import Base

class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    senha = Column(String, nullable=False)

    tipo = Column(String, default="usuario")

    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=True
    )

    empresa = relationship(
        "Empresa",
        back_populates="usuarios",
        foreign_keys=[empresa_id]
    )