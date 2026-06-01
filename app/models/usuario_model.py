from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from sqlalchemy.orm import relationship


class Usuario(Base):

######

    from sqlalchemy.orm import relationship

    avaliacoes = relationship(
    "Avaliacao",
    back_pop

######

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    # 🔹 Campos obrigatórios
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)

    # 🔹 Controle de acesso
    is_admin = Column(Boolean, default=False)

    avaliacoes = relationship(
    "Avaliacao",
    back_populates="usuario",
    cascade="all, delete-orphan"
)