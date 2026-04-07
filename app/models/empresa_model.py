from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    telefone = Column(String, nullable=True)

    cnpj = Column(String, nullable=True)
    cpf = Column(String, nullable=True)

    endereco = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    estado = Column(String, nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    ativo = Column(Boolean, default=True)
    avaliacao_media = Column(Float, default=0)

    # 🔗 RELACIONAMENTO COM TIPO DE SERVIÇO
    tipo_servico_id = Column(Integer, ForeignKey("tipos_servico.id"))
    tipo_servico = relationship("TipoServico", lazy="joined")

    fotos = relationship("EmpresaFoto", back_populates="empresa")