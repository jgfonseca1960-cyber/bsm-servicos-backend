from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

# =========================
# SERVIÇOS (TIPO)
# =========================
class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    # relacionamento com empresas
    empresas = relationship("Empresa", back_populates="servico")


# =========================
# EMPRESAS
# =========================

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String)
    cidade = Column(String)

    servico_id = Column(Integer, ForeignKey("servicos.id"))
    servico = relationship("Servico", back_populates="empresas")


# =========================
# USUÁRIOS
# =========================
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    senha = Column(String, nullable=False)
    tipo = Column(String)


# =========================
# FOTOS DA EMPRESA
# =========================
class EmpresaFoto(Base):
    __tablename__ = "empresa_fotos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)

    empresa_id = Column(Integer, ForeignKey("empresas.id"))