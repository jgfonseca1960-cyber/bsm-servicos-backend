from pydantic import BaseModel
from typing import Optional


class AvaliacaoBase(BaseModel):
    nota: int
    comentario: Optional[str] = None


class AvaliacaoCreate(AvaliacaoBase):
    empresa_id: int
    usuario_id: int


class AvaliacaoResponse(AvaliacaoBase):
    id: int

    empresa_id: int
    usuario_id: int

    class Config:
        from_attributes = True