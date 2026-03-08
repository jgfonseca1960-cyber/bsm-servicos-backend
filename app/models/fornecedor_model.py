from sqlalchemy import Column, Integer, String
from app.database import Base

class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)
    telefone = Column(String)
    cidade= Column(String)
    bairro= Column(String)
    responsavel= Column(String)
