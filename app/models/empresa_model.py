from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    # 🔹 dados básicos
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    telefone = Column(String, nullable=True)

    # 🔹 endereço
    endereco = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    cep = Column(String, nullable=True)

    # 🔹 localização (melhor manter como Float)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # 🔹 status
    ativo = Column(Boolean, default=True)
    avaliacao_media = Column(Float, nullable=True)

    # 🔹 documentos
    cpf = Column(String, nullable=True)
    cnpj = Column(String, nullable=True)

    # ✅ relacionamento (1 serviço → N empresas)
    servico_id = Column(
        Integer,
        ForeignKey("servicos.id"),
        nullable=True  # pode mudar para False depois
    )

    servico = relationship(
        "Servico",
        back_populates="empresas"
    )

    # ✅ relacionamento com fotos
    fotos = relationship(
        "EmpresaFoto",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )