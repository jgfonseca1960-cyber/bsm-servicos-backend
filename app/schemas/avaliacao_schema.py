from pydantic import BaseModel
from typing import Optional


class AvaliacaoCreate(BaseModel):
    empresa_id: int
    usuario_id: int
    nota: int
    comentario: Optional[str] = None