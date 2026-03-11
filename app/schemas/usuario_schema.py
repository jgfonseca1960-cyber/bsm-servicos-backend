from pydantic import BaseModel
from typing import Optional


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    tipo: Optional[str] = "cliente"
    empresa_id: Optional[int] = None


class UsuarioLogin(BaseModel):
    email: str
    senha: str


class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str
    tipo: str

    class Config:
        from_attributes = True