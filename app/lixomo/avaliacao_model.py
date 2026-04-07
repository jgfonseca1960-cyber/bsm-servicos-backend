from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Avaliacao(Base):

    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)

    nota = Column(Float)

    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id")
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=True
    )