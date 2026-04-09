from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)

    telefone = Column(String)
    whatsapp = Column(String)
    email = Column(String)

    endereco = Column(String)
    cep = Column(String)
    cidade = Column(String)
    estado = Column(String)

    servico_id = Column(Integer, ForeignKey("servicos.id"))

    servico = relationship("Servico", back_populates="empresas")

    fotos = relationship(
        "EmpresaFoto",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )