from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String)
    descricao = Column(String)
    telefone = Column(String)

    endereco = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    estado = Column(String)
    cep = Column(String)  # ✅ adicionando CEP

    latitude = Column(String)
    longitude = Column(String)

    ativo = Column(Boolean)
    avaliacao_media = Column(Float)

    cpf = Column(String)
    cnpj = Column(String)

    # relacionamento com serviço
    servico_id = Column(Integer, ForeignKey("servicos.id"))
    servico = relationship("Servico", back_populates="empresas")

    # relacionamento com fotos
    fotos = relationship(
        "EmpresaFoto",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )