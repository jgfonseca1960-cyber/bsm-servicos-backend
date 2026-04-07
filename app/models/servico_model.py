from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)

    # FK para empresa
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)

   