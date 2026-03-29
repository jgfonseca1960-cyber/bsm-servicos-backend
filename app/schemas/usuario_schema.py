from pydantic import BaseModel, EmailStr
from typing import Optional


# 🔹 Base (campos comuns)
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr


# 🔹 Para criação (entrada da API)
class UsuarioCreate(UsuarioBase):
    senha: str


# 🔹 Para atualização (PARCIAL)
class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None


# 🔹 Para resposta (saída da API)
class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True