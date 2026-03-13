from pydantic import BaseModel
from typing import Optional

class UsuarioLogin(BaseModel):
    email: str
    senha: str


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

c
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True