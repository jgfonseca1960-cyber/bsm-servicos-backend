from pydantic import BaseModel


class UsuarioCreate(BaseModel):

    email: str
    senha: str
    nome: str
    is_admin: bool


class UsuarioOut(BaseModel):

    id: int
    email: str
    nome: str

    class Config:
        from_attributes = True