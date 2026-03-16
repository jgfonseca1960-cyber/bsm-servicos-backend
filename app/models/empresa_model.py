from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Empresa(Base):

    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)

    descricao = Column(String)
    telefone = Column(String)
    endereco = Column(String)

    cidade = Column(String)
    estado = Column(String)
    bairro = Column(String)

    categoria = Column(String)
    tipo_servico = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )