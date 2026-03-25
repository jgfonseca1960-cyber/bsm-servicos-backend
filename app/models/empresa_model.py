from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Empresa(Base):

    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String)
    cnpj = Column(String)
    cpf = Column(String)
    responsavel = Column(String)
    telefone = Column(String)

    endereco = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    estado = Column(String)

    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    latitude = Column(Float)
    longitude = Column(Float)

    logo = Column(String)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=True
    )

    avaliacoes = relationship(
        "Avaliacao",
        back_populates="empresa",
        cascade="all, delete"
    )

    fotos = relationship(
        "Foto",
        back_populates="empresa",
        cascade="all, delete"
    )