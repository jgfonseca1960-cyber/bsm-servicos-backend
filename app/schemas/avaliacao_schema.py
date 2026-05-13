from pydantic import BaseModel


class AvaliacaoBase(BaseModel):
    nota: int
    comentario: str | None = None


class AvaliacaoCreate(AvaliacaoBase):
    empresa_id: int
    usuario_nome: str


class AvaliacaoResponse(AvaliacaoBase):
    id: int
    usuario_nome: str
    empresa_id: int

    class Config:
        from_attributes = True