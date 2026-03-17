from pydantic import BaseModel
from typing import Optional


class UsuarioCreate(BaseModel):

    nome: str
    email: str
    senha: str
    tipo: Optional[str] = "normal"


class UsuarioLogin(BaseModel):

    email: str
    senha: str