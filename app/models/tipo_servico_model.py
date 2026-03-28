from sqlalchemy import Column, Integer, String
from app.database import Base

class TipoServico(Base):
    __tablename__ = "tipos_servico"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)