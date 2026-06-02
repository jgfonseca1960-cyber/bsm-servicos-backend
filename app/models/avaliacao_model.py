from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from sqlalchemy import UniqueConstraint


class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True)
    empresa_id = Column(Integer, ForeignKey("empresa.id"))
    usuario_id = Column(Integer)
    nota = Column(Integer)
    comentario = Column(String)

    __table_args__ = (
        UniqueConstraint("empresa_id", "usuario_id", name="unique_user_empresa"),
    )

existing = db.query(Avaliacao).filter_by(
    empresa_id=empresa_id,
    usuario_id=usuario_id
).first()

if existing:
    raise HTTPException(
        status_code=400,
        detail="Usuário já avaliou esta empresa"
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