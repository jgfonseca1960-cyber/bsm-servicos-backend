from sqlalchemy import Column, Integer, String, ForeignKey
# from app.database import Base
from app.core.database import Base

class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    nota = Column(Integer)
    comentario = Column(String(300))