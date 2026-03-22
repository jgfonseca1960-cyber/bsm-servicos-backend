from sqlalchemy import Column, Integer, String, Float, ForeignKey
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

    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    latitude = Column(Float)
    longitude = Column(Float)

    logo = Column(String)