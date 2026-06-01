from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # 🔥 CORRETO (bate com seu banco real)
    senha_hash = Column(String, nullable=False)

    # 🔥 NOVO CAMPO DO BANCO
    is_admin = Column(Boolean, default=False)

    # ==========================================
    # ⭐ RELACIONAMENTO COM AVALIAÇÕES
    # ==========================================
    avaliacoes = relationship(
        "Avaliacao",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )