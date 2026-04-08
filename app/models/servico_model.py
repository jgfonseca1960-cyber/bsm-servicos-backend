from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    # 🔥 RELAÇÃO 1:N
    empresas = relationship(
        "Empresa",
        back_populates="servico"
    )