from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)
    responsavel = Column(String)
    telefone = Column(String)
    endereco = Column(String)

    cidade = Column(String)
    estado = Column(String)
    bairro = Column(String)

    tipo_servico = Column(String)
    categoria = Column(String)

    descricao = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)

    # ✅ ADICIONAR ISSO
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

     usuario = relationship(
        "Usuario",
        back_populates="empresas",
        foreign_keys=[usuario_id]
    )