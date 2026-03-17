from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Empresa(Base):

    __tablename__ = "empresas"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(String)

    cidade = Column(String)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )