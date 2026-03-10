from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey

from app.database import Base

class Empresa(Base):
    __tablename__ = "empresas"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200))
    responsavel = Column(String(150))
    telefone = Column(String(20))
    endereco = Column(String(200))
    tipo_servico = Column(String(100))
    cidade = Column(String(100))
    bairro = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    descricao = Column(Text)
    categoria = Column(Text)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))