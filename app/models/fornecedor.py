from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True)
    nome_empresa = Column(String(200))
    responsavel = Column(String(150))
    telefone = Column(String(20))
    descricao = Column(Text)
    cidade = Column(String(100))
    bairro = Column(String(100))