from pydantic import BaseModel, EmailStr
from typing import Optional


# 🔹 Base (campos comuns)
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr


# 🔹 Criação
class UsuarioCreate(UsuarioBase):
    senha: str
    is_admin: Optional[bool] = False


# 🔹 Atualização
class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    is_admin: Optional[bool] = None


# 🔹 Resposta
class UsuarioResponse(UsuarioBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True