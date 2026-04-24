from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class EmpresaFoto(Base):
    __tablename__ = "empresa_fotos"

    id = Column(Integer, primary_key=True, index=True)

    # 🔗 RELAÇÃO
    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id", ondelete="CASCADE"),  # 🔥 importante
        nullable=False
    )

    # 🖼 URL da imagem
    url = Column(String, nullable=False)

    # ⭐ FOTO PRINCIPAL
    principal = Column(Boolean, default=False, nullable=False)

    # ☁️ Cloudinary (IMPORTANTE pra deletar depois)
    public_id = Column(String, nullable=True)

    # 🔁 RELACIONAMENTO
    empresa = relationship(
        "Empresa",
        back_populates="fotos"
    )