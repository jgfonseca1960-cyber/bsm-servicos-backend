from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)

    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ⭐ Nota de 1 a 5 (recomendado)
    nota = Column(Integer, nullable=False)

    # ⭐ Limitar tamanho evita payload gigante
    comentario = Column(String(500), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # RELACIONAMENTOS
    empresa = relationship(
        "Empresa",
        back_populates="avaliacoes"
    )

    usuario = relationship(
        "Usuario",
        back_populates="avaliacoes"
    )