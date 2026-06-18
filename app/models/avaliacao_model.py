from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Text,
    UniqueConstraint
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    __table_args__ = (
        UniqueConstraint(
            "empresa_id",
            "usuario_id",
            name="uq_avaliacao_usuario_empresa"
        ),
    )

    id = Column(Integer, primary_key=True)

    empresa_id = Column(
        Integer,
        ForeignKey(
            "empresas.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    usuario_id = Column(
        Integer,
        ForeignKey(
            "usuarios.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    # =========================
    # AVALIAÇÃO
    # =========================

    nota = Column(
        Integer,
        nullable=False
    )

    comentario = Column(
        String(1000)
    )

    data_avaliacao = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # =========================
    # MODERAÇÃO
    # =========================

    status = Column(
        String(20),
        default="publicada"
    )
    # publicada
    # denunciada
    # removida
    # bloqueada

    suspeita = Column(
        Boolean,
        default=False
    )

    motivo_denuncia = Column(
        Text,
        nullable=True
    )

    denuncias = Column(
        Integer,
        default=0
    )

    # =========================
    # RESPOSTA EMPRESA
    # =========================

    resposta_empresa = Column(
        Text,
        nullable=True
    )

    data_resposta = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # =========================
    # AUDITORIA
    # =========================

    ip_origem = Column(
        String(100),
        nullable=True
    )

    user_agent = Column(
        String(500),
        nullable=True
    )

    # =========================
    # RELACIONAMENTOS
    # =========================

    empresa = relationship(
        "Empresa",
        back_populates="avaliacoes"
    )

    usuario = relationship(
        "Usuario",
        back_populates="avaliacoes"
    )