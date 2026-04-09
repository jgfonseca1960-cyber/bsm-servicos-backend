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
    cidade = Column(String)
    estado = Column(String)

    servico_id = Column(Integer, ForeignKey("servicos.id"))

    # 🔗 relacionamentos
    servico = relationship("Servico", back_populates="empresas")

    fotos = relationship(
        "Foto",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )