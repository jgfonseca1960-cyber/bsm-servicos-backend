from pydantic import BaseModel

class UsuarioCreate(BaseModel):

    nome: str
    email: str
    senha: str


class UsuarioResponse(BaseModel):

    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True