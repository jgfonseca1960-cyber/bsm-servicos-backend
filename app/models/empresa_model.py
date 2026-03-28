from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    # Dados básicos
    nome = Column(String, nullable=False)
    descricao = Column(String)

    # Contato
    telefone = Column(String)
    email = Column(String)

    # Documento (pode ser CPF ou CNPJ)
    cnpj = Column(String, unique=True, nullable=True)
    cpf = Column(String, unique=True, nullable=True)

    # Endereço
    endereco = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    estado = Column(String)

    # Localização (para mapa)
    latitude = Column(Float)
    longitude = Column(Float)

    # Status
    ativo = Column(Boolean, default=True)

    # Avaliação (média simples)
    avaliacao_media = Column(Float, default=0)

    # Relacionamentos
    servicos = relationship("Servico", back_populates="empresa")
    fotos = relationship("EmpresaFoto", back_populates="empresa")
⭐ SOBRE AVALIAÇÕES (IMPORTANTE)