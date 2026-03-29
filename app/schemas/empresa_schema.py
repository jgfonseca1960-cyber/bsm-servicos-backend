from pydantic import BaseModel
from typing import Optional


# 🔹 Base
class EmpresaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ativo: Optional[bool] = True


# 🔹 Criação
class EmpresaCreate(EmpresaBase):
    pass


# 🔹 Atualização
class EmpresaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ativo: Optional[bool] = None


# 🔹 Resposta
class EmpresaResponse(EmpresaBase):
    id: int

    class Config:
        from_attributes = True