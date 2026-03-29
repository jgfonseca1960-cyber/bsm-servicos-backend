from pydantic import BaseModel, EmailStr
from typing import Optional


# 🔹 Base
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    is_admin: Optional[bool] = False


# 🔹 Criação
class UsuarioCreate(UsuarioBase):
    senha: str


# 🔹 Atualização
class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    is_admin: Optional[bool] = None


# 🔹 Resposta
class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True