from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    # =====================================================
    # 🔹 DADOS BÁSICOS
    # =====================================================

    nome = Column(String, nullable=False)

    descricao = Column(String, nullable=True)

    telefone = Column(String, nullable=True)

    whatsapp = Column(String, nullable=True)

    email = Column(String, nullable=True)

    # =====================================================
    # 🔹 ENDEREÇO
    # =====================================================

    endereco = Column(String, nullable=True)

    bairro = Column(String, nullable=True)

    cidade = Column(String, nullable=True)

    estado = Column(String, nullable=True)

    cep = Column(String, nullable=True)

    # =====================================================
    # 🔹 GEOLOCALIZAÇÃO
    # =====================================================

    latitude = Column(Float, nullable=True)

    longitude = Column(Float, nullable=True)

    # =====================================================
    # 🔹 STATUS
    # =====================================================

    ativo = Column(
        Boolean,
        default=True,
        nullable=False
    )

    avaliacao_media = Column(
        Float,
        default=0.0
    )

    # =====================================================
    # 💰 MONETIZAÇÃO PREMIUM
    # =====================================================

    premium = Column(
        Boolean,
        default=False,
        nullable=False
    )

    destaque = Column(
        Boolean,
        default=False,
        nullable=False
    )

    plano = Column(
        String,
        default="gratuito"
    )

    prioridade = Column(
        Integer,
        default=0
    )

    whatsapp_destacado = Column(
        Boolean,
        default=False
    )

    exibir_no_topo = Column(
        Boolean,
        default=False
    )

    selo_premium = Column(
        Boolean,
        default=False
    )

    # =====================================================
    # 🔹 DOCUMENTOS
    # =====================================================

    cpf = Column(String, nullable=True)

    cnpj = Column(String, nullable=True)

    # =====================================================
    # 🔹 SERVIÇO
    # =====================================================

    servico_id = Column(
        Integer,
        ForeignKey(
            "servicos.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    servico = relationship(
        "Servico",
        back_populates="empresas"
    )

    # =====================================================
    # 🔹 FOTOS
    # =====================================================

    fotos = relationship(
        "EmpresaFoto",
        back_populates="empresa",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # =====================================================
    # ⭐ AVALIAÇÕES
    # =====================================================

    avaliacoes = relationship(
        "Avaliacao",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )

    # =====================================================
    # ⭐ FOTO PRINCIPAL (VIRTUAL)
    # =====================================================

    @property
    def foto_principal(self):

        if not self.fotos:
            return None

        for foto in self.fotos:

            if foto.principal:
                return foto.url

        return self.fotos[0].url

    # =====================================================
    # ⭐ TOTAL AVALIAÇÕES
    # =====================================================

    @property
    def total_avaliacoes(self):

        return len(self.avaliacoes)

    # =====================================================
    # ⭐ MÉDIA AVALIAÇÕES
    # =====================================================

    @property
    def media_avaliacoes(self):

        if not self.avaliacoes:
            return 0.0

        total = sum(a.nota for a in self.avaliacoes)

        return round(
            total / len(self.avaliacoes),
            1
        )

    # =====================================================
    # ⭐ EMPRESA PREMIUM
    # =====================================================

    @property
    def is_premium(self):

        return (
            self.premium or
            self.destaque or
            self.plano != "gratuito"
        )