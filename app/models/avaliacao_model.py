from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Avaliacao(Base):

    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True)

    nota = Column(Integer)

    comentario = Column(String)

    empresa_id = Column(Integer, ForeignKey("empresas.id"))