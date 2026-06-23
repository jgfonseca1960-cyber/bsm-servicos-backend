from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


# =========================================================
# BASE
# =========================================================

class AvaliacaoBase(BaseModel):
    nota: int
    comentario: Optional[str] = None


# =========================================================
# USUÁRIO RESUMIDO
# =========================================================

class UsuarioResumo(BaseModel):
    id: int
    nome: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# CREATE
# =========================================================

class AvaliacaoCreate(BaseModel):
    empresa_id: int
    usuario_id: int
    nota: int
    comentario: Optional[str] = None

    @field_validator("comentario")
    @classmethod
    def validar_comentario(cls, v, info):

        nota = info.data.get("nota")

        if nota is not None and nota <= 2:

            comentario = (v or "").strip()

            if len(comentario) < 20:
                raise ValueError(
                    "Avaliações com nota 1 ou 2 exigem "
                    "justificativa com pelo menos 20 caracteres."
                )

        return v


# =========================================================
# RESPONSE
# =========================================================

class AvaliacaoResponse(AvaliacaoBase):
    id: int

    empresa_id: int
    usuario_id: int

    # Usuário relacionado
    usuario: Optional[UsuarioResumo] = None

    # Moderação
    status: Optional[str] = "publicada"

    suspeita: bool = False

    denuncias: int = 0

    motivo_denuncia: Optional[str] = None

    # Resposta da empresa
    resposta_empresa: Optional[str] = None

    # Datas
    data_avaliacao: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )