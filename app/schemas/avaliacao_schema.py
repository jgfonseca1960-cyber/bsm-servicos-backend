from pydantic import BaseModel, field_validator
from typing import Optional


class AvaliacaoBase(BaseModel):
    nota: int
    comentario: Optional[str] = None


class AvaliacaoCreate(BaseModel):
    empresa_id: int
    nota: int
    comentario: str | None = None

    @field_validator("comentario")
    def validar_comentario(cls, v, info):
        nota = info.data.get("nota")

        if nota is not None and nota <= 2:
            if not v or len(v.strip()) < 20:
                raise ValueError(
                    "Avaliações com nota 1 ou 2 exigem justificativa com pelo menos 20 caracteres."
                )

        return v

class AvaliacaoResponse(AvaliacaoBase):
    id: int

    empresa_id: int
    usuario_id: int

    class Config:
        from_attributes = True