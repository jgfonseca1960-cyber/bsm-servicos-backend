from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.database import Base


class Empresa(Base):

    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String)
    cnpj = Column(String)
    cpf = Column(String)

    responsavel = Column(String)

    endereco = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    estado = Column(String)

    tipo_servico = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)

    avaliacao = Column(Float)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )