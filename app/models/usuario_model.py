from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)

    # ==========================================
    # ⭐ RELACIONAMENTO COM AVALIAÇÕES
    # ==========================================
    avaliacoes = relationship(
        "Avaliacao",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )