from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    # 🔹 dados básicos
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    telefone = Column(String, nullable=True)

    # 🔹 endereço
    endereco = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    cep = Column(String, nullable=True)

    # 🔹 localização
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # 🔹 status
    ativo = Column(Boolean, default=True, nullable=False)
    avaliacao_media = Column(Float, default=0.0)

    # 🔹 documentos
    cpf = Column(String, nullable=True)
    cnpj = Column(String, nullable=True)

    # 🔹 serviço
    servico_id = Column(
        Integer,
        ForeignKey("servicos.id", ondelete="SET NULL"),  # 🔥 importante
        nullable=True
    )

    servico = relationship(
        "Servico",
        back_populates="empresas"
    )

    # 🔹 fotos
    fotos = relationship(
        "EmpresaFoto",
        back_populates="empresa",
        cascade="all, delete-orphan",
        passive_deletes=True  # 🔥 melhora performance e integridade
    )

    # =========================
    # ⭐ FOTO PRINCIPAL (VIRTUAL)
    # =========================
    @property
    def foto_principal(self):
        """
        Retorna a foto principal da empresa (ou fallback)
        """
        if not self.fotos:
            return None

        # tenta pegar principal
        for f in self.fotos:
            if f.principal:
                return f.url

        # fallback: primeira foto
        return self.fotos[0].url