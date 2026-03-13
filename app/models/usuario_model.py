from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha = Column(String)

    tipo = Column(String, default="usuario")

    empresas = relationship(
        "Empresa",
        back_populates="usuario"
    )