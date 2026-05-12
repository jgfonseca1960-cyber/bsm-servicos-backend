from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database import Base
from datetime import datetime

class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    nota = Column(Integer)
    comentario = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)