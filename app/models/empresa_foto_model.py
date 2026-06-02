from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class EmpresaFoto(Base):
    __tablename__ = "empresa_fotos"

    id = Column(Integer, primary_key=True, index=True)

    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id", ondelete="CASCADE"),
        nullable=False
    )

    url = Column(String, nullable=False)

    principal = Column(Boolean, default=False, nullable=False)

    public_id = Column(String, nullable=True)

    empresa = relationship(
        "Empresa",
        back_populates="fotos"
    )