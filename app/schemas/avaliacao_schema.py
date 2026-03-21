from pydantic import BaseModel


class AvaliacaoCreate(BaseModel):

    nota: int
    comentario: str
    empresa_id: int


class AvaliacaoOut(BaseModel):

    id: int
    nota: int
    comentario: str
    empresa_id: int

    class Config:
        from_attributes = True