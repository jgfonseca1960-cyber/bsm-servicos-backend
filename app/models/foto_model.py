from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Foto(Base):

    __tablename__ = "fotos"

    id = Column(Integer, primary_key=True, index=True)

    caminho = Column(String)

    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id")
    )

    empresa = relationship(
        "Empresa",
        back_populates="fotos"
    )