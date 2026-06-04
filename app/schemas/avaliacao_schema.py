from pydantic import BaseModel, field_validator
from typing import Optional


class AvaliacaoBase(BaseModel):
    nota: int
    comentario: Optional[str] = None


class AvaliacaoCreate(BaseModel):
    empresa_id: int
    usuario_id: int
    nota: int
    comentario: str | None = None

    @field_validator("comentario")
    @classmethod
    def validar_comentario(cls, v, info):

        nota = info.data.get("nota")

        if nota is not None and nota <= 2:

            comentario = (v or "").strip()

            if len(comentario) < 20:
                raise ValueError(
                    "Avaliações com nota 1 ou 2 exigem justificativa com pelo menos 20 caracteres."
                )

        return v


class AvaliacaoResponse(AvaliacaoBase):
    id: int
    empresa_id: int
    usuario_id: int

    usuario: Optional[str] = None

    class Config:
        from_attributes = True