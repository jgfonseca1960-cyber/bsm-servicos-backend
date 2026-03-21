from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Avaliacao(Base):

    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)

    nota = Column(Integer)

    comentario = Column(String)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    empresa_id = Column(Integer, ForeignKey("empresas.id"))

    usuario = relationship("Usuario")

    empresa = relationship("Empresa")

    __table_args__ = (
        UniqueConstraint(
            "usuario_id",
            "empresa_id",
            name="unique_usuario_empresa"
        ),
    )