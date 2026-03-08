from pydantic import BaseModel

class AvaliacaoCreate(BaseModel):
    empresa_id: int
    usuario_id: int
    nota: int
    comentario: str

class AvaliacaoResponse(AvaliacaoCreate):
    id: int

    class Config:
        from_attributes = True